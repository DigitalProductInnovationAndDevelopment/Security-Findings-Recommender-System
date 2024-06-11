from typing import List, Set
from enum import Enum, auto

from src.data.Solution import Solution


class FindingKind(Enum):
    """
    An enum to represent the kind of finding.
    """
    SYSTEM = auto()
    USER = auto()
    CODE = auto()
    DEFAULT = auto()


class Finding:
    def __init__(self,
                 title: List[str] = {},
                 source: Set[str] = {},
                 description: List[str] = [],
                 cwe_ids: List[str] = [],
                 cve_ids: List[str] = [],
                 severity: int = None,
                 priority: int = None,
                 llm_service=None):
        """
        A class to represent a finding.
        :param title:  The title of the finding.
        :param source:  The source of the finding.
        :param description:  The description of the finding.
        :param cwe_ids:  The CWE IDs of the finding.
        :param cve_ids:  The CVE IDs of the finding.
        :param severity: The severity of the finding.
        :param priority:  The priority of the finding.
        :param llm_service:  The LLM service to use. Optional, will create a new one if not provided.
        """
        self.title = title
        self.source = source
        self.description = description
        self.cwe_ids = cwe_ids
        self.cve_ids = cve_ids
        self.severity = severity
        self.priority = priority
        self.category:FindingKind = FindingKind.DEFAULT

        self.solution = None

        self.llm_service = llm_service

    def add_category(self) -> 'Finding':
        from src.ai.LLMService import LLMService  # Lazy import to avoid circular imports
        if self.llm_service is None:
            self.llm_service = LLMService()
        self.category = self.llm_service.classify_kind(self)
        return self

    def generate_solution(self, long=True, short=True, search_term=True) -> 'Finding':
        if not short and not long:
            print("No solution requested, skipping generation. (But why would you do that?)")
            return self
        from src.ai.LLMService import LLMService
        if self.llm_service is None:
            self.llm_service = LLMService()
        short_str, long_str = "", ""
        search_terms = None
        if long:
            long_str = self.llm_service.get_recommendation(self, False)
        if short:
            short_str = self.llm_service.get_recommendation(self, True)
        if search_term:
            search_terms = self.llm_service.get_search_terms(self)
        self.solution = Solution(short_str, long_str, search_terms)

    def to_dict(self):
        data = {
            'title': self.title,
            'source': self.source,
            'description': self.description,
            'cwe_ids': self.cwe_ids,
            'cve_ids': self.cve_ids,
            'severity': self.severity,
            'priority': self.priority,
        }
        if self.category is not None and self.category != FindingKind.DEFAULT:
            data['category'] = self.category.name

        if self.solution is not None:
            data['solution'] = self.solution.to_dict()
        return data

    def __str__(self):
        result = ""

        #Finding
        result+="-------    Finding    -------\n"
        if len(self.title) > 0:
            result += f"Title: {', '.join(self.title)}\n"
        if len(self.source) > 0:
            result += f"Source: {', '.join(self.source)}\n"
        if len(self.description) > 0:
            result += f"Description: {', '.join(self.description)}\n"
        if len(self.cwe_ids) > 0:
            result += f"CWE IDs: {', '.join(self.cwe_ids)}\n"
        if len(self.cve_ids) > 0:
            result += f"CVE IDs: {', '.join(self.cve_ids)}\n"
        if self.severity is not None:
            result += f"Severity: {self.severity}\n"
        if self.priority is not None:
            result += f"Priority: {self.priority}\n"
        if self.category is not None and self.category != FindingKind.DEFAULT:
            result += f"Category: {self.category.name}\n"

        #Solution
        if self.solution is not None:
            result += f"{str(self.solution)}"

        return result

    def to_html(self, table = False):
        result = f"<h3>{','.join(self.cve_ids)}</h3>"

        # make a table
        if table:
            result += "<table>"
            result += "<tr><th>Name</th><th>Value</th></tr>"
            result += f"<tr><td>Title</td><td>{', '.join(self.title)}</td></tr>"
            result += f"<tr><td>Source</td><td>{', '.join(self.source)}</td></tr>"
            result += f"<tr><td>Description</td><td>{', '.join(self.description)}</td></tr>"
            result += f"<tr><td>CWE IDs</td><td>{', '.join(self.cwe_ids)}</td></tr>"
            result += f"<tr><td>CVE IDs</td><td>{', '.join(self.cve_ids)}</td></tr>"
            result += f"<tr><td>Severity</td><td>{self.severity}</td></tr>"
            result += f"<tr><td>Priority</td><td>{self.priority}</td></tr>"
            if self.category is not None and self.category != FindingKind.DEFAULT:
                result += f"<tr><td>Category</td><td>{self.category.name}</td></tr>"
            result += "</table>"
        else:
            result += "<h3>Finding</h3>"
            result += f"<p>Title: {', '.join(self.title)}</p>"
            result += f"<p>Source: {', '.join(self.source)}</p>"
            result += f"<p>Description: {', '.join(self.description)}</p>"
            result += f"<p>CWE IDs: {', '.join(self.cwe_ids)}</p>"
            result += f"<p>CVE IDs: {', '.join(self.cve_ids)}</p>"
            result += f"<p>Severity: {self.severity}</p>"
            result += f"<p>Priority: {self.priority}</p>"
            if self.category is not None and self.category != FindingKind.DEFAULT:
                result += f"<p>Category: {self.category.name}</p>"

        if self.solution is not None:
            result += f"{self.solution.to_html()}"


        return result