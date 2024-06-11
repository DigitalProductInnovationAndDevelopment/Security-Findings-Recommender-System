from typing import List, Dict, Union, Optional
import os
import json
import logging
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.utils.text_tools import clean
from src.data.Finding import Finding, FindingKind
from src.ai.prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
    CONVERT_DICT_TO_STR_TEMPLATE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """
    This class is a wrapper around the OLLAMA API. It provides methods for generating recommendations and search terms
    for security findings, as well as classifying the kind of finding.
    """

    def __init__(self, model_url: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the LLMService object.
        :param model_url: The URL of the OLLAMA model. If not provided, it will be read from the environment variable OLLAMA_URL or default to http://localhost:11434.
        :param model_name:  The name of the OLLAMA model. If not provided, it will be read from the environment variable OLLAMA_MODEL or default to llama3:instruct.
        """
        # Configure logging level for httpx
        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Now, variables
        if model_url is None:
            model_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.pull_url: str = model_url + "/api/pull"
        self.generate_url: str = model_url + "/api/generate"
        self.model_name: str = model_name or os.getenv("OLLAMA_MODEL", "llama3:instruct")

        self.generate_payload: Dict[str, Union[str, bool]] = {
            "model": self.model_name,
            "stream": False,
            "format": "json",
        }

        # and finally, init functions
        self.init_pull_model()

    def init_pull_model(self) -> None:
        """
        ATTENTION: If the model is not cached, this function might take a long time to execute (depending on your internet connection).
        Pull the model from the OLLAMA server.
        :return: None
        """
        payload = {"name": self.model_name}
        response = httpx.post(self.pull_url, json=payload)
        response.raise_for_status()

    def get_model_name(self) -> str:
        """
        Get the name of the OLLAMA model.
        :return:  The name of the OLLAMA model.
        """
        return self.model_name

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60))
    def generate(self, prompt: str) -> Dict[str, str]:
        """
        Generate a response from the OLLAMA model given a prompt.
        :param prompt:  The prompt to generate a response for.
        :return: The response from the OLLAMA model.
        """
        payload = {
            "prompt": prompt,
            **self.generate_payload
        }
        try:
            # Set the timeout to 300 seconds (5 minutes). On m1, it usually takes 20 seconds.
            timeout = httpx.Timeout(timeout=300.0)
            response = httpx.post(self.generate_url, json=payload, timeout=timeout)
            response.raise_for_status()
            try:
                json_response = response.json()
                return json.loads(json_response['response'], strict=False)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                return {}
        except httpx.ReadTimeout as e:
            logger.warning(f"ReadTimeout occurred: {e}")
            return {}

    def classify_kind(self, finding: Finding, options: Optional[List[FindingKind]] = None) -> FindingKind:
        """
        Classify the kind of security finding.
        :param finding: The finding to classify.
        :param options: The options to choose from. If not provided, all options are available.
        :return: The classified kind of finding.
        """
        if options is None:
            options = list(FindingKind)

        options_str = ', '.join([kind.name for kind in options])
        prompt = CLASSIFY_KIND_TEMPLATE.format(options=options_str, data=str(finding))
        response = self.generate(prompt)
        if 'selected_option' not in response:
            logger.warning(f"Failed to classify the finding: {finding.title}")
            return FindingKind.DEFAULT
        return FindingKind[response['selected_option']]

    def get_recommendation(self, finding: Finding, short: bool = True) -> Union[str, List[str]]:
        """
        Generate a recommendation for the security finding.
        Adds to metadata of the finding: used_meta_prompt, prompt_short, prompt_long
        :param finding:  The finding to generate a recommendation for.
        :param short:  Whether to generate a short recommendation or a long one.
        :return: The recommendation for the finding.
        """
        if short:
            prompt = SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        else:
            if finding.solution and finding.solution.short_description:
                finding.solution.add_to_metadata("used_meta_prompt", True)
                prompt = self._generate_prompt_with_meta_prompts(finding)
            else:
                prompt = GENERIC_LONG_RECOMMENDATION_TEMPLATE

        finding.solution.add_to_metadata(f"prompt_{'short' if short else 'long'}", prompt)
        response = self.generate(prompt)

        if 'recommendation' not in response:
            error_message = f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}"
            logger.error(error_message)
            return '[SYSTEM] Failed to generate recommendation.' if short else [
                '[SYSTEM] Failed to generate recommendation.']

        return clean(response['recommendation'])

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        """
        Generate a prompt for the long recommendation based on the short recommendation.
        :param finding: The finding to generate a prompt for.
        :return: The prompt for the long recommendation.
        """
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(category=finding.category.name,
                                                                      short_recommendation=short_recommendation)
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get('meta_prompts', ''))

        return LONG_RECOMMENDATION_TEMPLATE.format(short_recommendation=short_recommendation, meta_prompts=meta_prompts)

    def get_search_terms(self, finding: Finding) -> str:
        """
        Generate search terms for future research into the security finding.
        :param finding: The finding to generate search terms for.
        :return: The search terms for the finding.
        """
        prompt = SEARCH_TERMS_TEMPLATE.format(data=str(finding))
        response = self.generate(prompt)
        if 'search_terms' not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return ""
        return clean(response['search_terms'])

    def convert_dict_to_str(self, data):
        """
        Convert a dictionary to a string.
        :param data: The dictionary to convert.
        :return: The string representation of the dictionary.
        """
        prompt = CONVERT_DICT_TO_STR_TEMPLATE.format(data=json.dumps(data))
        response = self.generate(prompt)
        if 'converted_text' not in response:
            logger.info(f"Failed to convert dictionary to string, returning it as str conversion.")
            return str(data)
        return clean(response['converted_text'])
