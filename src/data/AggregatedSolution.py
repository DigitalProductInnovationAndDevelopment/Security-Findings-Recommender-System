from typing import List

from data.Finding import Finding
from pydantic import BaseModel


class AggregatedSolution(BaseModel):
    findings: List[Finding] = None
    solution: str = ""
    metadata: dict = {}

    def from_result(self, findings: List[Finding], solution: str, metadata=None):
        self.findings = findings
        self.solution = solution
        self.metadata = metadata
        return self

    def __str__(self):
        return self.solution

    def to_dict(self):
        return {
            "findings": [finding.to_dict() for finding in self.findings],
            "solution": self.solution,
            "metadata": self.metadata,
        }

    def to_html(self):
        return f"<p>{self.solution}</p>"
