# This tests the interworkings of the LLMServiceStrategy, VulnerabilityReport, and Finding classes.
# This does not necessarily test the functionality of the LLM Models, but rather the interactions between the classes.

from ai.LLM import BaseLLMService, LLMServiceMixin
from data.Finding import Finding


from typing import List, Dict, Union, Tuple

from ai.LLM.BaseLLMService import BaseLLMService
from ai.LLM.LLMServiceMixin import LLMServiceMixin
from utils.text_tools import clean
from data.Finding import Finding
from ai.LLM.Strategies.ollama_prompts import (
    CLASSIFY_KIND_TEMPLATE,
    SHORT_RECOMMENDATION_TEMPLATE,
    LONG_RECOMMENDATION_TEMPLATE,
    META_PROMPT_GENERATOR_TEMPLATE,
    GENERIC_LONG_RECOMMENDATION_TEMPLATE,
    SEARCH_TERMS_TEMPLATE,
    AGGREGATED_SOLUTION_TEMPLATE,
    SUBDIVISION_PROMPT_TEMPLATE,
    answer_in_json_prompt,
)


class MockLLMService(BaseLLMService, LLMServiceMixin):
    def __init__(
        self,
    ):

        self.model_url = "mock"
        self.model_name = "mock_model"
        self.context_size = 8000

        LLMServiceMixin.__init__(
            self, {"model_url": self.model_url, "model_name": self.model_name}
        )

        self.pull_url: str = self.model_url + "/api/pull"
        self.generate_url: str = self.model_url + "/api/generate"
        self.generate_payload: Dict[str, Union[str, bool]] = {
            "model": self.model_name,
            "stream": False,
            "format": "json",
        }

    def init_pull_model(self) -> None:
        pass

    def get_model_name(self) -> str:
        return self.model_name

    def get_context_size(self) -> int:
        return self.context_size

    def get_url(self) -> str:
        return self.generate_url

    def _generate(self, prompt: str, json=True) -> Dict[str, str]:
        # TODO: Mock Aggregated Solution Responses and Subdivision Responses
        print(f"{answer_in_json_prompt('recommendation')}".format())
        if f"{answer_in_json_prompt('combined_description').format()}" in prompt:
            return {"combined_description": "combined_description"}
        if f"{answer_in_json_prompt('selected_option').format()}" in prompt:
            return {"selected_option": "JavaScript"}
        if f"{answer_in_json_prompt('recommendation').format()}" in prompt:
            return {"recommendation": "recommendation_response"}

        if f"{answer_in_json_prompt('search_terms').format()}" in prompt:
            return {"search_terms": "search_terms_response"}
        if "Convert the following dictionary to a descriptive string" in prompt:
            return {"response": "dict_to_str_response"}

        return {}

    def _get_classification_prompt(
        self, options: str, field_name: str, finding_str: str
    ) -> str:
        return CLASSIFY_KIND_TEMPLATE.format(
            options=options, field_name=field_name, data=finding_str
        )

    def _get_recommendation_prompt(self, finding: Finding, short: bool) -> str:
        if short:
            return SHORT_RECOMMENDATION_TEMPLATE.format(data=str(finding))
        elif finding.solution and finding.solution.short_description:
            finding.solution.add_to_metadata("used_meta_prompt", True)
            return self._generate_prompt_with_meta_prompts(finding)
        else:
            return GENERIC_LONG_RECOMMENDATION_TEMPLATE.format()

    def _process_recommendation_response(
        self, response: Dict[str, str], finding: Finding, short: bool
    ) -> Union[str, List[str]]:
        if "recommendation" not in response:

            return "" if short else [""]
        return clean(response["recommendation"], llm_service=self)

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
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

    def _get_search_terms_prompt(self, finding: Finding) -> str:
        return SEARCH_TERMS_TEMPLATE.format(data=str(finding))

    def _process_search_terms_response(
        self, response: Dict[str, str], finding: Finding
    ) -> str:
        if "search_terms" not in response:

            return ""
        return clean(response["search_terms"], llm_service=self)

    def _get_subdivision_prompt(self, findings: List[Finding]) -> str:
        findings_str = self._get_findings_str_for_aggregation(findings)
        return SUBDIVISION_PROMPT_TEMPLATE.format(data=findings_str)

    def _process_subdivision_response(
        self, response: Dict, findings: List[Finding]
    ) -> List[Tuple[List[Finding], Dict]]:
        pass

    def _get_aggregated_solution_prompt(
        self, findings: List[Finding], meta_info: Dict
    ) -> str:
        findings_str = self._get_findings_str_for_aggregation(findings, details=True)

        return AGGREGATED_SOLUTION_TEMPLATE.format(
            data=findings_str, meta_info=meta_info.get("reason", "")
        )

    def _process_aggregated_solution_response(self, response: Dict[str, str]) -> str:
        if "aggregated_solution" not in response:
            raise "Failed to generate an aggregated solution"
        return clean(response["aggregated_solution"], llm_service=self)

    def convert_dict_to_str(self, data: Dict) -> str:

        return LLMServiceMixin.convert_dict_to_str(self, data)

    def combine_descriptions(
        self,
        descriptions: List[str],
    ) -> str:
        return "combined_description"
