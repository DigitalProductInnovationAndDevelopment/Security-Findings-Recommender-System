import json
import os
from typing import Dict, List, Optional, Union

import openai

from ai.LLM.BaseLLMService import BaseLLMService
from data.Finding import FindingKind, Finding
from ai.LLM.Strategies.openai_prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
    CONVERT_DICT_TO_STR_TEMPLATE, META_PROMPT_GENERATOR_TEMPLATE, LONG_RECOMMENDATION_TEMPLATE
)
from utils.text_tools import clean

import logging
logger = logging.getLogger(__name__)


class OpenAIService(BaseLLMService):
    def __init__(self, api_key: str = os.getenv("OPENAI_API_KEY", None), model: str = "gpt-4o"):
        if api_key is None:
            raise ValueError("API key not provided and OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key
        self.model = model

    def get_model_name(self) -> str:
        return self.model

    def get_url(self) -> str:
        return "-"

    def generate(self, prompt: str) -> Dict[str, str]:
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        return {"response": content}

    def classify_kind(self, finding: Finding, options: Optional[List[FindingKind]] = None) -> FindingKind:
        if options is None:
            options = list(FindingKind)

        options_str = ', '.join([kind.name for kind in options])
        prompt = CLASSIFY_KIND_TEMPLATE.format(options=options_str, data=str(finding))
        response = self.generate(prompt)
        if 'response' not in response:
            logger.warning(f"Failed to classify the finding: {finding.title}")
            return FindingKind.DEFAULT
        return FindingKind[response['response'].strip()]

    def get_recommendation(self, finding: Finding, short: bool = True) -> Union[str, List[str]]:
        if short:
            prompt = SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        else:  # long recommendation
            if finding.solution and finding.solution.short_description:
                finding.solution.add_to_metadata("used_meta_prompt", True)
                prompt = self._generate_prompt_with_meta_prompts(finding)
            else:
                prompt = GENERIC_LONG_RECOMMENDATION_TEMPLATE

        finding.solution.add_to_metadata(f"prompt_{'short' if short else 'long'}", prompt)
        response = self.generate(prompt)

        if 'response' not in response:
            logger.warning(
                f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}")
            return '' if short else ['']

        return clean(response['response'], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(finding=str(finding))
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(
            meta_prompt_response.get("response", ""), llm_service=self
        )

        long_prompt = LONG_RECOMMENDATION_TEMPLATE.format(meta_prompts=meta_prompts)

        finding.solution.add_to_metadata("prompt_long_breakdown", {
            "short_recommendation": short_recommendation,
            "meta_prompts": meta_prompts
        })

        return long_prompt

    def get_search_terms(self, finding: Finding) -> str:
        prompt = SEARCH_TERMS_TEMPLATE.format(data=str(finding))
        response = self.generate(prompt)
        if 'response' not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return ""
        return clean(response['response'], llm_service=self)

    def convert_dict_to_str(self, data) -> str:
        prompt = CONVERT_DICT_TO_STR_TEMPLATE.format(data=json.dumps(data))
        response = self.generate(prompt)
        if 'response' not in response:
            logger.info(f"Failed to convert dictionary to string, returning it as str conversion.")
            return str(data)
        return clean(response['response'], llm_service=self)
