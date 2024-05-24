import pandas as pd

from data.types import Content


def from_content_list(content_list: list[Content]) -> 'Findings':
    df = pd.DataFrame(content_list)
    return Findings(df)


class Findings:
    def __init__(self, findings):
        self.findings = findings

    def get_findings(self):
        return self.findings
