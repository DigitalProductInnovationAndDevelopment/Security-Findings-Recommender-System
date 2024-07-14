import json
from enum import Enum
from typing import Dict, List, Optional, Union

import openai

from ai.LLM.BaseLLMService import BaseLLMService
from ai.LLM.LLMServiceMixin import LLMServiceMixin
from data.Finding import Finding
from ai.LLM.Strategies.openai_prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
)
from utils.text_tools import clean

from config import config

import logging

logger = logging.getLogger(__name__)


class OpenAIService(BaseLLMService, LLMServiceMixin):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the OpenAIService.

        Args:
            api_key (Optional[str]): OpenAI API key. If None, falls back to config.
            model (str): OpenAI model name. Defaults to "gpt-4".
        """
        self.api_key = api_key or config.openai_api_key
        self.model = model

        if self.api_key is None:
            raise ValueError(
                "API key not provided and OPENAI_API_KEY environment variable not set."
            )

        LLMServiceMixin.__init__(self, {
            'api_key': self.api_key,
            'model': self.model
        })
        openai.api_key = self.api_key

    def get_model_name(self) -> str:
        return self.model

    def get_url(self) -> str:
        return "-"

    def _generate(self, prompt: str) -> Dict[str, str]:
        try:
            response = openai.chat.completions.create(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            return {"response": content}
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
        if "response" not in response:
            logger.warning(
                f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}")
            return "" if short else [""]
        return clean(response["response"], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(finding=str(finding))
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get("response", ""), llm_service=self)

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
        if "response" not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return ""
        return clean(response["response"], llm_service=self)

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
