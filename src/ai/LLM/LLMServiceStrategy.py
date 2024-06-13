from typing import Dict, Optional, List

from ai.LLM.BaseLLMService import BaseLLMService
from data.Finding import Finding, FindingKind


class LLMServiceStrategy:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    def generate(self, prompt: str) -> Dict[str, str]:
        return self.llm_service.generate(prompt)

    def classify_kind(self, finding: Finding, options: Optional[List[FindingKind]] = None) -> FindingKind:
        return self.llm_service.classify_kind(finding, options)

    def get_recommendation(self, finding: Finding, short: bool = True) -> str:
        return self.llm_service.get_recommendation(finding, short)

    def get_search_terms(self, finding: Finding) -> str:
        return self.llm_service.get_search_terms(finding)

    def convert_dict_to_str(self, data) -> str:
        return self.llm_service.convert_dict_to_str(data)
