from enum import Enum
from typing import Dict, Optional, List, Union, Tuple

from ai.LLM.BaseLLMService import BaseLLMService
from data.Finding import Finding


class LLMServiceStrategy:
    def __init__(self, llm_service: BaseLLMService):
        """
        Initialize the LLMServiceStrategy.

        Args:
            llm_service (BaseLLMService): An instance of a class inheriting from BaseLLMService.
        """
        if not isinstance(llm_service, BaseLLMService):
            raise ValueError("llm_service must be an instance of a class inheriting from BaseLLMService")
        self.llm_service = llm_service

    def get_model_name(self) -> str:
        """Get the name of the current LLM model."""
        return self.llm_service.get_model_name()

    def get_context_size(self) -> int:
        """Get the context size of the current LLM service."""
        return self.llm_service.get_context_size()

    def get_url(self) -> str:
        """Get the URL associated with the current LLM service."""
        return self.llm_service.get_url()

    def generate(self, prompt: str) -> Dict[str, str]:
        """
        Generate a response using the current LLM service.

        Args:
            prompt (str): The input prompt.

        Returns:
            Dict[str, str]: The generated response.
        """
        return self.llm_service.generate(prompt)

    def combine_descriptions(self, descriptions: List[str], cve_ids, cwe_ids) -> str:
        """
        Combine multiple descriptions into a single, coherent description.

        Args:
            descriptions (List[str]): The list of descriptions to combine.
            cve_ids (List[str]): The list of CVE IDs.
            cwe_ids (List[str]): The list of CWE IDs.

        Returns:
            str: The combined description.
        """
        return self.llm_service.combine_descriptions(
            descriptions + [f" CVE IDs: {cve_ids} CWE IDs: {cwe_ids}"])  # I apologize for this, it's a hack

    def classify_kind(self, finding: Finding, field_name: str, options: Optional[List[Enum]] = None) -> Optional[Enum]:
        """
        Classify the kind of finding.

        Args:
            finding (Finding): The finding to classify.
            field_name (str): The name of the field to classify.
            options (Optional[List[Enum]]): The possible classification options.

        Returns:
            Optional[Enum]: The classified kind, or None if classification failed.
        """
        return self.llm_service.classify_kind(finding, field_name, options)

    def get_recommendation(self, finding: Finding, short: bool = True) -> Union[str, List[str]]:
        """
        Get a recommendation for a finding.

        Args:
            finding (Finding): The finding to get a recommendation for.
            short (bool): Whether to get a short or long recommendation.

        Returns:
            Union[str, List[str]]: The generated recommendation.
        """
        return self.llm_service.get_recommendation(finding, short)

    def get_search_terms(self, finding: Finding) -> str:
        """
        Get search terms for a finding.

        Args:
            finding (Finding): The finding to get search terms for.

        Returns:
            str: The generated search terms.
        """
        return self.llm_service.get_search_terms(finding)

    def generate_aggregated_solution(self, findings: List[Finding]) -> List[Tuple[str, List[Finding], Dict]]:
        """
        Generate an aggregated solution for a group of findings.

        Args:
            findings (List[Finding]): The findings to generate a solution for.

        Returns:
            List[Tuple[str, List[Finding], Dict]]: The generated solution, the findings it applies to, and any additional metadata
        """
        return self.llm_service.generate_aggregated_solution(findings)

    def convert_dict_to_str(self, data: Dict) -> str:
        """
        Convert a dictionary to a string representation.

        Args:
            data (Dict): The dictionary to convert.

        Returns:
            str: The string representation of the dictionary.
        """
        return self.llm_service.convert_dict_to_str(data)
