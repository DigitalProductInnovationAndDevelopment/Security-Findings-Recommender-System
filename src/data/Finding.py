from typing import List, Set, Optional, Any
from enum import Enum, auto
from pydantic import BaseModel, Field, PrivateAttr
from data.Solution import Solution
import json


class FindingKind(Enum):
    """
    An enum to represent the kind of finding.
    """

    SYSTEM = "system"
    PROGRAM = "program"
    LIBRARY = "library"
    USER = "user"
    CODE = "code"
    DEFAULT = "default"


class Finding(BaseModel):
    title: List[str] = Field(default_factory=list)
    source: Set[str] = Field(default_factory=set)
    description: List[str] = Field(default_factory=list)
    cwe_ids: List[str] = Field(default_factory=list)
    cve_ids: List[str] = Field(default_factory=list)
    severity: Optional[int] = None
    priority: Optional[int] = None
    location_list: List[str] = Field(default_factory=list)
    category: FindingKind = FindingKind.DEFAULT
    solution: Optional["Solution"] = None
    _llm_service: Optional[Any] = PrivateAttr(default=None)

    def add_category(self) -> "Finding":
        from ai.LLM.LLMServiceStrategy import (
            LLMServiceStrategy,
        )  # Lazy import to avoid circular imports

        if self.llm_service is None:
            self.llm_service = LLMServiceStrategy()
        self.category = self.llm_service.classify_kind(self)
        return self

    @property
    def llm_service(self) -> Optional[Any]:
        return self._llm_service

    @llm_service.setter
    def llm_service(self, value: Optional[Any]):
        self._llm_service = value

    def from_json(self, d: dict) -> "Finding":
        """
        Load the finding from a JSON(finding) dictionary.
        """
        self.title = [x["element"] for x in d["title_list"]]
        self.source = set([x["source"] for x in d["title_list"]])
        self.description = [x["element"] for x in d.get("description_list", [])]
        self.cwe_ids = [", ".join(x["element"]) for x in d.get("cwe_id_list", [])]
        self.cve_ids = (
            [x["element"] for x in d.get("cve_id_list", [])]
            if "cve_id_list" in d
            else []
        )
        self.severity = d.get("severity", None)
        self.priority = d.get("priority", None)

        locations = []
        for loc in d.get("location_list", []):
            try:
                location = json.loads(
                    loc["location"].replace("'", '"')
                )  # This is a hack to fix the single quotes in the JSON
            except json.JSONDecodeError:
                locations.append(loc["location"])
                continue

            file = location.get("file", "")
            line = location.get("line", "")
            column = location.get("column", "")

            location_str = f"{file}:{line}, {column}"

            locations.append(location_str)

        self.location_list = locations
        return self

    def generate_solution(self, long=True, short=True, search_term=True) -> "Finding":
        if not short and not long:
            print(
                "No solution requested, skipping generation. (But why would you do that?)"
            )
            return self
        from ai.LLM.LLMServiceStrategy import LLMServiceStrategy

        if self.llm_service is None:
            self.llm_service = LLMServiceStrategy()
        self.solution = Solution()
        if short:
            short_solution = self.llm_service.get_recommendation(self, True)
            self.solution.set_short_description(short_solution)
        if long:
            self.solution.set_long_description(
                self.llm_service.get_recommendation(self, False)
            )
        if search_term:
            self.solution.set_search_terms(self.llm_service.get_search_terms(self))

    def to_dict(self):
        data = {
            "title": self.title,
            "source": list(self.source),
            "location_list": self.location_list,
            "description": self.description,
            "cwe_ids": self.cwe_ids,
            "cve_ids": self.cve_ids,
            "severity": self.severity,
            "priority": self.priority,
        }
        if self.category is not None and self.category != FindingKind.DEFAULT:
            data["category"] = self.category.name

        if self.solution is not None:
            data["solution"] = self.solution.to_dict()
        return data

    def __str__(self):
        result = ""

        # Finding
        result += "-------    Security Finding    -------\n"
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
            result += (
                f"<tr><td>Description</td><td>{', '.join(self.description)}</td></tr>"
            )
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
                result += (
                    f"<p>Location List: {' & '.join(map(str, self.location_list))}</p>"
                )
            result += f"<p>CWE IDs: {', '.join(self.cwe_ids)}</p>"
            result += f"<p>CVE IDs: {', '.join(self.cve_ids)}</p>"
            result += f"<p>Severity: {self.severity}</p>"
            result += f"<p>Priority: {self.priority}</p>"
            if self.category is not None and self.category != FindingKind.DEFAULT:
                result += f"<p>Category: {self.category.name}</p>"

        if self.solution is not None:
            result += f"{self.solution.to_html()}"

        return result
