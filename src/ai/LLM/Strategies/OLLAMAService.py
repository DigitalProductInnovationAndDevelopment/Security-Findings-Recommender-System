from typing import List, Dict, Union, Optional
import logging
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ai.LLM.BaseLLMService import BaseLLMService
from ai.LLM.LLMServiceMixin import LLMServiceMixin
from utils.json_helper import parse_json
from utils.text_tools import clean
from data.Finding import Finding
from ai.LLM.Strategies.ollama_prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE, COMBINE_DESCRIPTIONS_TEMPLATE,
)
from config import config

logger = logging.getLogger(__name__)


class OLLAMAService(BaseLLMService, LLMServiceMixin):
    def __init__(
            self,
            model_url: Optional[str] = None,
            model_name: Optional[str] = None
    ):
        """
        Initialize the OLLAMAService.

        Args:
            model_url (Optional[str]): The URL of the OLLAMA model. If None, uses config.
            model_name (Optional[str]): The name of the OLLAMA model. If None, uses config.
        """
        self.model_url = model_url or config.ollama_url
        self.model_name = model_name or config.ollama_model
        self.context_size = 8000

        LLMServiceMixin.__init__(self, {
            'model_url': self.model_url,
            'model_name': self.model_name
        })

        self.pull_url: str = self.model_url + "/api/pull"
        self.generate_url: str = self.model_url + "/api/generate"
        self.generate_payload: Dict[str, Union[str, bool]] = {
            "model": self.model_name,
            "stream": False,
            "format": "json",
        }
        self.init_pull_model()

    def init_pull_model(self) -> None:
        """Pull the model from the OLLAMA server."""
        payload = {"name": self.model_name}
        try:
            response = httpx.post(
                self.pull_url, json=payload, timeout=60 * 10
            )
            response.raise_for_status()
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to the OLLAMA server: {e}")
            logger.info(f"Ollama URL is {self.pull_url}")

    def get_model_name(self) -> str:
        return self.model_name

    def get_context_size(self) -> int:
        return self.context_size

    def get_url(self) -> str:
        return self.generate_url

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    def _generate(self, prompt: str) -> Dict[str, str]:
        payload = {"prompt": prompt, **self.generate_payload}
        try:
            timeout = httpx.Timeout(timeout=300.0)
            response = httpx.post(self.generate_url, json=payload, timeout=timeout)
            response.raise_for_status()
            json_response = response.json()
            return parse_json(json_response["response"], strict=False)
        except httpx.ReadTimeout as e:
            logger.warning(f"ReadTimeout occurred: {e}")
            return {}
        except Exception as e:
            return self.handle_api_error(e)

    def _get_classification_prompt(self, options: str, field_name: str, finding_str: str) -> str:
        return CLASSIFY_KIND_TEMPLATE.format(options=options, field_name=field_name, data=finding_str)

    def _get_recommendation_prompt(self, finding: Finding, short: bool) -> str:
        if short:
            return SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        elif finding.solution and finding.solution.short_description:
            finding.solution.add_to_metadata("used_meta_prompt", True)
            return self._generate_prompt_with_meta_prompts(finding)
        else:
            return GENERIC_LONG_RECOMMENDATION_TEMPLATE

    def _process_recommendation_response(self, response: Dict[str, str], finding: Finding, short: bool) -> Union[
        str, List[str]]:
        if "recommendation" not in response:
            logger.warning(
                f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}")
            return "" if short else [""]
        return clean(response["recommendation"], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(finding=str(finding))
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get("meta_prompts", ""), llm_service=self)

        long_prompt = LONG_RECOMMENDATION_TEMPLATE.format(meta_prompts=meta_prompts)

        finding.solution.add_to_metadata(
            "prompt_long_breakdown",
            {
                "short_recommendation": short_recommendation,
                "meta_prompts": meta_prompts,
            },
        )

        return long_prompt

    def _get_search_terms_prompt(self, finding: Finding) -> str:
        return SEARCH_TERMS_TEMPLATE.format(data=str(finding))

    def _process_search_terms_response(self, response: Dict[str, str], finding: Finding) -> str:
        if "search_terms" not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return ""
        return clean(response["search_terms"], llm_service=self)

    def convert_dict_to_str(self, data: Dict) -> str:
        """
        Convert a dictionary to a string representation.

        This method uses the implementation from LLMServiceMixin.

        Args:
            data (Dict): The dictionary to convert.

        Returns:
            str: The string representation of the dictionary.
        """
        return LLMServiceMixin.convert_dict_to_str(self, data)

    def combine_descriptions(self, descriptions: List[str]) -> str:
        """
        Combine multiple descriptions into a single, coherent description.

        Args:
            descriptions (List[str]): The list of descriptions to combine.

        Returns:
            str: The combined description.
        """
        if len(descriptions) <= 1:
            return descriptions[0] if descriptions else ""

        prompt = COMBINE_DESCRIPTIONS_TEMPLATE.format(data=descriptions)

        response = self.generate(prompt)
        if "combined_description" in response:
            return self.clean_response(response["combined_description"])
        else:
            logger.warning("Failed to combine descriptions")
            return " ".join(descriptions)
