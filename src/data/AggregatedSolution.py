from typing import List

from data.Finding import Finding
from db.base import BaseModel


class AggregatedSolution:
    findings: List[Finding] = None
    solution: str = ""
    metadata: dict = {}

    def __init__(self, findings: List[Finding], solution: str, metadata=None):
        self.findings = findings
        self.solution = solution
        self.metadata = metadata

    def __str__(self):
        return self.solution

    def to_dict(self):
        return {
            "findings": [finding.to_dict() for finding in self.findings],
            "solution": self.solution,
            "metadata": self.metadata
        }

    def to_html(self):
        return f"<p>{self.solution}</p>"