from __future__ import annotations
from typing import List, Dict, Union, Optional
import os
import json
import logging
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.Finding import Finding, FindingKind
from src.ai.prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean(text: str | List[str], split_paragraphs=False) -> str | List[str]:
    if isinstance(text, list):
        # strip and if in the first 5 chars there is a ':', remove everything before it
        flattened = [item for sublist
                     in [clean(t).split("\n\n")
                         if split_paragraphs
                         else [clean(t)] for t in text]
                     for item in sublist]
        return flattened
    if isinstance(text, float):
        print(f"Float found: {text}")  # Why would there be a float? Noone knows. But it happened, so we are prepared.
        return str(text)
    if isinstance(text, dict):  # Also happened. LLMs are unpredictable.
        print(f"Dict found: {text}")
        return str(text)  # TODO: Here, we could use the llm to convert it more smartly.
    return text.strip()


class LLMService:
    def __init__(self, model_url: Optional[str] = None, model_name: Optional[str] = None):
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
        payload = {"name": self.model_name}
        response = httpx.post(self.pull_url, json=payload)
        response.raise_for_status()

    def get_model_name(self) -> str:
        return self.model_name

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60))
    def generate(self, prompt: str) -> Dict[str, str]:
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
                logger.error(f"Failed to parse JSON response: {e}")
                return {}
        except httpx.ReadTimeout as e:
            logger.error(f"ReadTimeout occurred: {e}")
            return {}

    def classify_kind(self, finding: Finding, options: Optional[List[FindingKind]] = None) -> FindingKind:
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
            logger.warning(error_message)
            return '[SYSTEM] Failed to generate recommendation.' if short else [
                '[SYSTEM] Failed to generate recommendation.']

        return clean(response['recommendation'])

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = META_PROMPT_GENERATOR_TEMPLATE.format(category=finding.category.name,
                                                                      short_recommendation=short_recommendation)
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get('meta_prompts', ''))

        return LONG_RECOMMENDATION_TEMPLATE.format(short_recommendation=short_recommendation, meta_prompts=meta_prompts)

    def get_search_terms(self, finding: Finding) -> List[str]:
        prompt = SEARCH_TERMS_TEMPLATE.format(data=str(finding))
        response = self.generate(prompt)
        if 'search_terms' not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return []
        return clean(response['search_terms'])
