from typing import List
from collections import defaultdict
from data.Finding import Finding
from utils.token_utils import fits_in_context


class FindingBatcher:
    """
    Class to batch findings based on the LLM's context size.
    """
    def __init__(self, llm_service):
        """
        Initialize the FindingBatcher with the LLM service and category attributes.
        :param llm_service:  The LLM service.
        """
        self.llm_service = llm_service
        self.category_attributes = [
            'security_aspect', 'affected_component', 'technology_stack',
            'remediation_type', 'severity_level', 'compliance', 'environment'
        ]

    def create_batches(self, findings: List[Finding]) -> List[List[Finding]]:
        """Create batches of findings that fit within the LLM's context."""
        if self._fits_in_context(findings, include_solution=True):
            return [findings]
        elif self._fits_in_context(findings, include_solution=False):
            return [self._strip_solutions(findings)]
        return self._recursive_batch(findings)

    def _recursive_batch(self, findings: List[Finding], depth: int = 0) -> List[List[Finding]]:
        """Recursively batch findings based on category attributes."""
        if depth >= len(self.category_attributes):
            return self._final_split(findings)

        grouped = self._group_by_attribute(findings, self.category_attributes[depth])
        batches = []

        for group in grouped.values():
            if len(group) == 1:
                # batches.append(group)
                pass  # Remove single findings, as they are not useful for *aggregated* solutions
            elif self._fits_in_context(group, include_solution=True):
                batches.append(group)
            elif self._fits_in_context(group, include_solution=False):
                batches.append(self._strip_solutions(group))
            else:
                batches.extend(self._recursive_batch(group, depth + 1))

        return batches

    def _group_by_attribute(self, findings: List[Finding], attribute: str) -> dict:
        """Group findings by a specific category attribute."""
        grouped = defaultdict(list)
        for finding in findings:
            if finding.category and getattr(finding.category, attribute):
                key = getattr(finding.category, attribute).value
            else:
                key = 'unknown'
            grouped[key].append(finding)
        return grouped

    def _final_split(self, findings: List[Finding]) -> List[List[Finding]]:
        """Split findings when all category attributes have been exhausted."""
        batches = []
        current_batch = []

        for finding in findings:
            current_batch.append(finding)
            if self._fits_in_context(current_batch, include_solution=True):
                continue
            elif self._fits_in_context(current_batch, include_solution=False):
                current_batch = self._strip_solutions(current_batch)
            else:
                # If adding this finding exceeds the context, start a new batch
                batches.append(current_batch[:-1])
                current_batch = [finding]

        if current_batch:
            batches.append(current_batch)

        return batches

    def _fits_in_context(self, findings: List[Finding], include_solution: bool) -> bool:
        """Check if a list of findings fits within the LLM's context."""
        content = "\n".join(self._finding_to_string(f, include_solution) for f in findings)
        return fits_in_context(content, self.llm_service)

    def _finding_to_string(self, finding: Finding, include_solution: bool) -> str:
        """Convert a finding to a string representation."""
        content = f"Description: {finding.description}"
        if include_solution and finding.solution:
            content += f"\nSolution: {finding.solution.short_description}"
        return content

    def _strip_solutions(self, findings: List[Finding]) -> List[Finding]:
        """Remove solutions from a list of findings."""
        return [Finding(**{**f.dict(), 'solution': None}) for f in findings]
