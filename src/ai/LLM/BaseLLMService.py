from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Union

from data.Finding import Finding, FindingKind


class BaseLLMService(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def generate(self, prompt: str) -> Dict[str, str]:
        pass

    @abstractmethod
    def classify_kind(self, finding: Finding, options: Optional[List[FindingKind]] = None) -> FindingKind:
        pass

    @abstractmethod
    def get_recommendation(self, finding: Finding, short: bool = True) -> str:
        pass

    @abstractmethod
    def get_search_terms(self, finding: Finding) -> str:
        pass

    @abstractmethod
    def convert_dict_to_str(self, data) -> str:
        pass
