from typing import List, Set
from enum import Enum, auto

from data.Solution import Solution


class FindingKind(Enum):
    """
    An enum to represent the kind of finding.
    """
    SYSTEM = auto()
    PROGRAM = auto()
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
                 location_list: List[str] = None,
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
        :param location_list: The list of locations for the finding.
        :param llm_service:  The LLM service to use. Optional, will create a new one if not provided.
        """
        self.title = title
        self.source = source
        self.description = description
        self.cwe_ids = cwe_ids
        self.cve_ids = cve_ids
        self.severity = severity
        self.priority = priority
        self.location_list = location_list or []
        self.category: FindingKind = FindingKind.DEFAULT

        self.solution = None

        self.llm_service = llm_service

    def add_category(self) -> 'Finding':
        from ai.LLM.LLMServiceStrategy import LLMServiceStrategy  # Lazy import to avoid circular imports
        if self.llm_service is None:
            self.llm_service = LLMServiceStrategy()
        self.category = self.llm_service.classify_kind(self)
        return self

    def generate_solution(self, long=True, short=True, search_term=True) -> 'Finding':
        if not short and not long:
            print("No solution requested, skipping generation. (But why would you do that?)")
            return self
        from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
        if self.llm_service is None:
            self.llm_service = LLMServiceStrategy()
        self.solution = Solution()
        if short:
            short_solution = self.llm_service.get_recommendation(self, True)
            self.solution.set_short_description(short_solution)
        if long:
            self.solution.set_long_description(self.llm_service.get_recommendation(self, False))
        if search_term:
            self.solution.set_search_terms(self.llm_service.get_search_terms(self))

    def to_dict(self):
        data = {
            'title': self.title,
            'source': list(self.source),
            'location_list': self.location_list,
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

        # Finding
        result += "-------    Finding    -------\n"
        if len(self.title) > 0:
            result += f"Title: {', '.join(self.title)}\n"
        if len(self.source) > 0:
            result += f"Source: {', '.join(self.source)}\n"
        if len(self.description) > 0:
            result += f"Description: {', '.join(self.description)}\n"
        if len(self.location_list) > 0:
            result += f"Location List:\n"
            for location in self.location_list:
                result += f"  - {location}\n"
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

        # Solution
        if self.solution is not None:
            result += f"{str(self.solution)}"

        return result

    def to_html(self, table=False):
        result = f"<h3>{','.join(self.cve_ids)}</h3>"

        # make a table
        if table:
            result += "<table>"
            result += "<tr><th>Name</th><th>Value</th></tr>"
            result += f"<tr><td>Title</td><td>{', '.join(self.title)}</td></tr>"
            result += f"<tr><td>Source</td><td>{', '.join(self.source)}</td></tr>"
            result += f"<tr><td>Description</td><td>{', '.join(self.description)}</td></tr>"
            if len(self.location_list) > 0:
                result += f"<tr><td>Location List</td><td>{' & '.join(map(str, self.location_list))}</td></tr>"
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
            if len(self.location_list) > 0:
                result += f"<p>Location List: {' & '.join(map(str, self.location_list))}</p>"
            result += f"<p>CWE IDs: {', '.join(self.cwe_ids)}</p>"
            result += f"<p>CVE IDs: {', '.join(self.cve_ids)}</p>"
            result += f"<p>Severity: {self.severity}</p>"
            result += f"<p>Priority: {self.priority}</p>"
            if self.category is not None and self.category != FindingKind.DEFAULT:
                result += f"<p>Category: {self.category.name}</p>"

        if self.solution is not None:
            result += f"{self.solution.to_html()}"

        return result
