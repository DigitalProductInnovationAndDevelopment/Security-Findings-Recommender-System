from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional, List, Union, Tuple
import logging

from data.Finding import Finding

logger = logging.getLogger(__name__)


class BaseLLMService(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_context_size(self) -> int:
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

    def generate_aggregated_solution(self, findings: List[Finding]) -> List[Tuple[str, List[Finding], Dict]]:
        """
        Generate an aggregated solution for a group of findings.

        Args:
            findings (List[Finding]): The findings to generate a solution for.

        Returns:
            List[Tuple[str, List[Finding], Dict]]: The generated solution, the findings it applies to, and any additional metadata
        """
        finding_groups = self._subdivide_finding_group(findings)
        if len(finding_groups) < 1:
            return []  # No suitable groups found

        results = []

        for group, meta_info in finding_groups:
            prompt = self._get_aggregated_solution_prompt(group, meta_info)
            response = self.generate(prompt)
            solution = self._process_aggregated_solution_response(response)

            if solution:
                results.append((solution, group, meta_info))

        return results

    def _get_findings_str_for_aggregation(self, findings, details=False) -> str:
        findings_str = ''
        for id, finding in enumerate(findings):
            findings_str += f"{id + 1}. \n"
            findings_str += finding.description.replace('\n', ' ') + '\n'
            if details:
                findings_str += "Locations: " ",".join(finding.location_list)
                findings_str += str(finding.category) + '\n'
            if finding.solution:
                findings_str += finding.solution.short_description.replace('\n', ' ') + '\n\n'
        return findings_str

    def _subdivide_finding_group(self, findings: List[Finding]) -> List[Tuple[List[Finding], Dict]]:
        prompt = self._get_subdivision_prompt(findings)
        response = self.generate(prompt)
        return self._process_subdivision_response(response, findings)

    @abstractmethod
    def _get_subdivision_prompt(self, findings: List[Finding]) -> str:
        pass

    @abstractmethod
    def _process_subdivision_response(self, response: Dict, findings: List[Finding]) -> List[
        Tuple[List[Finding], Dict]]:
        pass

    @abstractmethod
    def _get_aggregated_solution_prompt(self, findings: List[Finding], meta_info: Dict) -> str:
        pass

    @abstractmethod
    def _process_aggregated_solution_response(self, response: Dict) -> str:
        pass

    @abstractmethod
    def convert_dict_to_str(self, data) -> str:
        pass
