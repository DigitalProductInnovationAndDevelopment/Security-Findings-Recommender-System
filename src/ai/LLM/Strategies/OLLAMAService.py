from typing import List, Dict, Union, Optional
import os
import json
import logging
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ai.LLM.BaseLLMService import BaseLLMService
from utils.json_helper import parse_json
from utils.text_tools import clean
from data.Finding import Finding, FindingKind
from ai.LLM.Strategies.ollama_prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
    CONVERT_DICT_TO_STR_TEMPLATE,
)

from config import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def is_up() -> bool:
    # res = requests.post(os.getenv('OLLAMA_URL') + '/api/show', json={'name': os.getenv('OLLAMA_MODEL', 'llama3')})
    res = httpx.post(
        config.ollama_url + "/api/show",
        json={"name": config.ollama_model},
    )
    if res.status_code == 200:
        return True
    else:
        return False


@singleton
class OLLAMAService(BaseLLMService):
    """
    This class is a wrapper around the OLLAMA API. It provides methods for generating recommendations and search terms
    for security findings, as well as classifying the kind of finding.
    """

    def __init__(
        self, model_url: Optional[str] = None, model_name: Optional[str] = None
    ):
        """
        Initialize the LLMService object.
        :param model_url: The URL of the OLLAMA model. If not provided, it will be read from the environment variable OLLAMA_URL or default to http://localhost:11434.
        :param model_name:  The name of the OLLAMA model. If not provided, it will be read from the environment variable OLLAMA_MODEL or default to llama3:instruct.
        """
        # Configure logging level for httpx
        logging.getLogger("httpx").setLevel(logging.WARNING)
        # Now, variables
        if model_url is None:
            model_url = config.ollama_url
        self.pull_url: str = model_url + "/api/pull"
        self.generate_url: str = model_url + "/api/generate"
        self.model_name: str = model_name or config.ollama_model

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
        try:
            response = httpx.post(
                self.pull_url, json=payload, timeout=60 * 10
            )  # 10 minutes timeout
            response.raise_for_status()
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to the OLLAMA server: {e}")
            logger.info(f"Ollama URL is {self.pull_url}")

    def get_model_name(self) -> str:
        """
        Get the name of the OLLAMA model.
        :return:  The name of the OLLAMA model.
        """
        return self.model_name

    def get_url(self) -> str:
        """
        Get the URL of the OLLAMA model.
        :return: The URL of the OLLAMA model.
        """
        return self.generate_url

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    def generate(self, prompt: str) -> Dict[str, str]:
        """
        Generate a response from the OLLAMA model given a prompt.
        :param prompt:  The prompt to generate a response for.
        :return: The response from the OLLAMA model.
        """
        payload = {"prompt": prompt, **self.generate_payload}

        try:
            # Set the timeout to 300 seconds (5 minutes). On my Mac M1, OLLAMA (llama3:7b) usually takes 30 seconds.
            timeout = httpx.Timeout(timeout=300.0)
            response = httpx.post(self.generate_url, json=payload, timeout=timeout)
            response.raise_for_status()
            try:
                json_response = response.json()
                return parse_json(json_response["response"], strict=False)
            except json.JSONDecodeError as e:
                logger.error(
                    f"LLM-Models JSON response is malformed, could not be parsed: {e}"
                )
                return {}
        except httpx.ReadTimeout as e:
            logger.warning(f"ReadTimeout occurred: {e}")
            return {}

    def classify_kind(
        self, finding: Finding, options: Optional[List[FindingKind]] = None
    ) -> FindingKind:
        """
        Classify the kind of security finding.
        :param finding: The finding to classify.
        :param options: The options to choose from. If not provided, all options are available.
        :return: The classified kind of finding.
        """
        if options is None:
            options = list(FindingKind)

        options_str = ", ".join([kind.name for kind in options])
        prompt = CLASSIFY_KIND_TEMPLATE.format(options=options_str, data=str(finding))
        response = self.generate(prompt)
        if "selected_option" not in response:
            logger.warning(f"Failed to classify the finding: {finding.title}")
            return FindingKind.DEFAULT
        try:
            return FindingKind[response["selected_option"]]
        except KeyError:
            logger.error(
                f"Failed to classify the finding: {finding.title}. "
                f"Selected option: {response['selected_option']} does not exist in FindingKind."
                f"Returning default kind."
            )
            return FindingKind.DEFAULT

    def get_recommendation(self, finding: Finding, short: bool = True) -> str:
        """
        Generate a recommendation for the security finding.
        Adds to metadata of the finding: used_meta_prompt, prompt_short, prompt_long
        :param finding:  The finding to generate a recommendation for.
        :param short:  Whether to generate a short recommendation or a long one.
        :return: The recommendation for the finding.
        """
        prompt = ""
        if short:
            prompt = SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        if not short:  # long recommendation
            if finding.solution and finding.solution.short_description:
                finding.solution.add_to_metadata("used_meta_prompt", True)
                prompt = self._generate_prompt_with_meta_prompts(finding)
            else:
                prompt = GENERIC_LONG_RECOMMENDATION_TEMPLATE

        finding.solution.add_to_metadata(
            f"prompt_{'short' if short else 'long'}", prompt
        )
        response = self.generate(prompt)

        if "recommendation" not in response:
            logger.info(
                f"Failed to generate a {'short' if short else 'long'} recommendation for a finding. Trying once more..."
            )
            response = self.generate(prompt)
        if "recommendation" not in response:
            if short:
                logger.warning(
                    f"Failed again to generate a {'short' if short else 'long'} recommendation for the finding. Trying one last time...."
                )
                response = self.generate(prompt)
            else:
                logger.warning(
                    f"Failed again to generate a {'short' if short else 'long'} recommendation for the finding. Trying with generic prompt..."
                )
                finding.solution.add_to_metadata(
                    f"fallback_to_generic_long_prompt", True
                )
                response = self.generate(GENERIC_LONG_RECOMMENDATION_TEMPLATE)
        if "recommendation" not in response:
            logger.error(
                f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}"
            )
            return "" if short else [""]

        return clean(response["recommendation"], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        """
        Generate a prompt for the long recommendation based on the short recommendation.
        :param finding: The finding to generate a prompt for.
        :return: The prompt for the long recommendation.
        """
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(
            finding=str(finding)
        )
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(
            meta_prompt_response.get("meta_prompts", ""), llm_service=self
        )

        long_prompt = LONG_RECOMMENDATION_TEMPLATE.format(meta_prompts=meta_prompts)

        finding.solution.add_to_metadata(
            "prompt_long_breakdown",
            {
                "short_recommendation": short_recommendation,
                "meta_prompts": meta_prompts,
            },
        )

        return long_prompt

    def get_search_terms(self, finding: Finding) -> str:
        """
        Generate search terms for future research into the security finding.
        :param finding: The finding to generate search terms for.
        :return: The search terms for the finding.
        """
        prompt = SEARCH_TERMS_TEMPLATE.format(data=str(finding))
        response = self.generate(prompt)
        if "search_terms" not in response:
            logger.warning(
                f"Failed to generate search terms for the finding: {finding.title}"
            )
            return ""
        return clean(response["search_terms"], llm_service=self)

    def convert_dict_to_str(self, data):
        """
        Convert a dictionary to a string.
        :param data: The dictionary to convert.
        :return: The string representation of the dictionary.
        """
        prompt = CONVERT_DICT_TO_STR_TEMPLATE.format(data=json.dumps(data))
        response = self.generate(prompt)
        if "converted_text" not in response:
            logger.info(
                f"Failed to convert dictionary to string, returning it as str conversion."
            )
            return str(data)
        return clean(response["converted_text"], llm_service=self)
