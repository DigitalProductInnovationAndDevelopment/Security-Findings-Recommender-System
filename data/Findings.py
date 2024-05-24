import pandas as pd

from data.types import Content


class Findings:
    def __init__(self, findings: list[Content]):
        self.findings = findings

    def get_findings(self):
        return self.findings
