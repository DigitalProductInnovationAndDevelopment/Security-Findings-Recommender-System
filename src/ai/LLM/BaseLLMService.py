from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional, List, Union
import logging

from data.Finding import Finding

logger = logging.getLogger(__name__)


class BaseLLMService(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def _generate(self, prompt: str) -> Dict[str, str]:
        pass

    def generate(self, prompt: str) -> Dict[str, str]:
        try:
            return self._generate(prompt)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {"error": str(e)}

    @abstractmethod
    def combine_descriptions(self, descriptions: List[str]) -> str:
        pass

    def classify_kind(self, finding: Finding, field_name: str, options: Optional[List[Enum]] = None) -> Optional[Enum]:
        if options is None:
            logger.warning(f"No options provided for field {field_name}")
            return None

        options_str = ", ".join([option.value for option in options])
        prompt = self._get_classification_prompt(options_str, field_name, str(finding))
        response = self.generate(prompt)

        return self._process_classification_response(response, field_name, finding, options_str, options)

    @abstractmethod
    def _get_classification_prompt(self, options: str, field_name: str, finding_str: str) -> str:
        pass

    def _process_classification_response(self, response: Dict[str, str], field_name: str, finding: Finding,
                                         options_str: str, options: List[Enum]) -> Optional[Enum]:
        if "selected_option" not in response:
            logger.warning(f"Failed to classify the {field_name} for the finding: {finding.title}")
            return None
        if response["selected_option"] in ["None", "NotListed"]:
            logger.info(f"Chose None for {field_name} for the finding: {finding.title}")
            return None
        if response["selected_option"] not in options_str:
            logger.warning(f"Failed to classify the {field_name} for the finding: {finding.title}")
            return None

        return next(option for option in options if option.value == response["selected_option"])

    def get_recommendation(self, finding: Finding, short: bool = True) -> Union[str, List[str]]:
        prompt = self._get_recommendation_prompt(finding, short)
        finding.solution.add_to_metadata(f"prompt_{'short' if short else 'long'}", prompt)
        response = self.generate(prompt)

        return self._process_recommendation_response(response, finding, short)

    @abstractmethod
    def _get_recommendation_prompt(self, finding: Finding, short: bool) -> str:
        pass

    @abstractmethod
    def _process_recommendation_response(self, response: Dict[str, str], finding: Finding, short: bool) -> Union[
        str, List[str]]:
        pass

    def get_search_terms(self, finding: Finding) -> str:
        prompt = self._get_search_terms_prompt(finding)
        response = self.generate(prompt)
        return self._process_search_terms_response(response, finding)

    @abstractmethod
    def _get_search_terms_prompt(self, finding: Finding) -> str:
        pass

    @abstractmethod
    def _process_search_terms_response(self, response: Dict[str, str], finding: Finding) -> str:
        pass

    @abstractmethod
    def convert_dict_to_str(self, data) -> str:
        pass
