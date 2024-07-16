import json
import re
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum

from anthropic import Anthropic

from ai.LLM.BaseLLMService import BaseLLMService
from ai.LLM.LLMServiceMixin import LLMServiceMixin
from data.Finding import Finding
from ai.LLM.Strategies.openai_prompts import (
    OPENAI_CLASSIFY_KIND_TEMPLATE,
    OPENAI_SHORT_RECOMMENDATION_TEMPLATE,
    OPENAI_GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    OPENAI_SEARCH_TERMS_TEMPLATE,
    OPENAI_META_PROMPT_GENERATOR_TEMPLATE,
    OPENAI_LONG_RECOMMENDATION_TEMPLATE,
    OPENAI_COMBINE_DESCRIPTIONS_TEMPLATE,
    OPENAI_AGGREGATED_SOLUTION_TEMPLATE, OPENAI_SUBDIVISION_PROMPT_TEMPLATE,
)
from utils.text_tools import clean
from config import config

import logging

logger = logging.getLogger(__name__)


class AnthropicService(BaseLLMService, LLMServiceMixin):
    """
    AnthropicService class for interacting with Anthropic's language models.

    This class implements the BaseLLMService and uses the LLMServiceMixin
    to provide Anthropic-specific functionality.
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "claude-3-5-sonnet-20240620"
    ):
        """
        Initialize the AnthropicService.

        Args:
            api_key (Optional[str]): Anthropic API key. If None, falls back to config.
            model (str): Anthropic model name. Defaults to "claude-3-5-sonnet-20240620".
        """
        self.api_key = api_key or config.anthropic_api_key
        self.model = model
        self.context_size = 200000

        if self.api_key is None:
            raise ValueError(
                "API key not provided and ANTHROPIC_API_KEY environment variable not set."
            )

        LLMServiceMixin.__init__(self, {
            'api_key': self.api_key,
            'model': self.model
        })
        self.client = Anthropic(api_key=self.api_key)

    def get_model_name(self) -> str:
        """Get the name of the Anthropic model being used."""
        return "-".join(self.model.split("-")[:-1])

    def get_context_size(self) -> int:
        """Get the context size for the Anthropic API."""
        return self.context_size

    def get_url(self) -> str:
        """Get the URL for the Anthropic API (placeholder method)."""
        return "-"

    def _generate(self, prompt: str, json=False) -> Dict[str, str]:
        """
        Generate a response using the Anthropic API.

        Args:
            prompt (str): The input prompt.

        Returns:
            Dict[str, str]: A dictionary containing the generated response.
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            if json:
                messages.append({"role": "assistant", "content": "Here is the JSON requested:\n{"})
            message = self.client.messages.create(
                max_tokens=1024,
                messages=messages,
                model=self.model,
            )
            content = message.content[0].text
            if json:
                content = "{" + content
            return {"response": content}
        except Exception as e:
            return self.handle_api_error(e)

    def _get_classification_prompt(self, options: str, field_name: str, finding_str: str) -> str:
        """Generate the classification prompt for Anthropic."""
        return OPENAI_CLASSIFY_KIND_TEMPLATE.format(options=options, field_name=field_name, data=finding_str)

    def _get_recommendation_prompt(self, finding: Finding, short: bool) -> str:
        """Generate the recommendation prompt for Anthropic."""
        if short:
            return OPENAI_SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        elif finding.solution and finding.solution.short_description:
            finding.solution.add_to_metadata("used_meta_prompt", True)
            return self._generate_prompt_with_meta_prompts(finding)
        else:
            return OPENAI_GENERIC_LONG_RECOMMENDATION_TEMPLATE

    def _process_recommendation_response(self, response: Dict[str, str], finding: Finding, short: bool) -> Union[
        str, List[str]]:
        """Process the recommendation response from Anthropic."""
        if "response" not in response:
            logger.warning(
                f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}")
            return "" if short else [""]
        return clean(response["response"], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        """Generate a prompt with meta-prompts for long recommendations."""
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = OPENAI_META_PROMPT_GENERATOR_TEMPLATE.format(finding=str(finding))
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get("response", ""), llm_service=self)

        long_prompt = OPENAI_LONG_RECOMMENDATION_TEMPLATE.format(meta_prompts=meta_prompts)

        finding.solution.add_to_metadata(
            "prompt_long_breakdown",
            {
                "short_recommendation": short_recommendation,
                "meta_prompts": meta_prompts,
            },
        )

        return long_prompt

    def _get_search_terms_prompt(self, finding: Finding) -> str:
        """Generate the search terms prompt for Anthropic."""
        return OPENAI_SEARCH_TERMS_TEMPLATE.format(data=str(finding))

    def _process_search_terms_response(self, response: Dict[str, str], finding: Finding) -> str:
        """Process the search terms response from Anthropic."""
        if "response" not in response:
            logger.warning(f"Failed to generate search terms for the finding: {finding.title}")
            return ""
        return clean(response["response"], llm_service=self)

    def _get_subdivision_prompt(self, findings: List[Finding]) -> str:
        findings_str = self._get_findings_str_for_aggregation(findings)
        return OPENAI_SUBDIVISION_PROMPT_TEMPLATE.format(data=findings_str)

    def _process_subdivision_response(self, response: Dict[str, str], findings: List[Finding]) -> List[Tuple[List[Finding], Dict]]:
        if "response" not in response:
            logger.warning("Failed to subdivide findings")
            return [(findings, {})]  # Return all findings as a single group if subdivision fails

        try:
            response = response["response"]
            # remove prefix ```json and suffix ```
            response = re.sub(r'^```json', '', response)
            response = re.sub(r'```$', '', response)
            subdivisions = json.loads(response)["subdivisions"]
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response")
            return [(findings, {})]
        except KeyError:
            logger.error("Unexpected JSON structure in response")
            return [(findings, {})]

        result = []
        for subdivision in subdivisions:
            try:
                group_indices = [int(i.strip()) - 1 for i in subdivision["group"].split(',')]
                group = [findings[i] for i in group_indices if i < len(findings)]
                meta_info = {"reason": subdivision.get("reason", "")}
                if len(group) == 1:
                    continue  # Skip single-element groups for *aggregated* solutions
                result.append((group, meta_info))
            except ValueError:
                logger.error(f"Failed to parse group indices: {subdivision['group']}")
                continue
            except KeyError:
                logger.error("Unexpected subdivision structure")
                continue

        return result

    def _get_aggregated_solution_prompt(self, findings: List[Finding], meta_info: Dict) -> str:
        findings_str = self._get_findings_str_for_aggregation(findings, details=True)
        return OPENAI_AGGREGATED_SOLUTION_TEMPLATE.format(
            data=findings_str,
            meta_info=meta_info.get("reason", "")
        )

    def _process_aggregated_solution_response(self, response: Dict[str, str]) -> str:
        if "response" not in response:
            logger.warning("Failed to generate an aggregated solution")
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

        prompt = OPENAI_COMBINE_DESCRIPTIONS_TEMPLATE.format(data=descriptions)

        response = self.generate(prompt)
        if "response" not in response:
            return descriptions[0]
        return clean(response["response"], llm_service=self)
