from typing import Optional, Dict
from pydantic import BaseModel, Field


class Solution(BaseModel):
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    search_terms: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)

    def set_short_description(self, short_description: str):
        self.short_description = short_description

    def set_long_description(self, long_description: str):
        self.long_description = long_description

    def set_search_terms(self, search_terms: str):
        self.search_terms = search_terms

    def add_to_metadata(self, key: str, value):
        self.metadata = {f"{key}": value, **self.metadata}

    def to_dict(self):
        return {
            "short_description": self.short_description,
            "long_description": self.long_description,
            "search_terms": self.search_terms if self.search_terms is not None else "",
            "metadata": self.metadata,
        }

    def __str__(self):
        if (
                (self.short_description is None)
                and (self.long_description is None)
                and (self.search_terms is None)
        ):
            return ""
        result = ""
        result += "-------    Solution    -------\n"
        if self.short_description is not None:
            result += f"Short Description: {self.short_description}\n"
        if self.long_description is not None:
            result += f"Long Description: {self.long_description}\n"
        if self.search_terms is not None:
            result += f"Search Terms: {self.search_terms}\n"
        return result

    def to_html(self, table=False):
        result = ""
        if table:
            result += "<table>"
            result += "<tr><th>Solution</th></tr>"
            result += (
                f"<tr><td>Short Description</td><td>{self.short_description}</td></tr>"
            )
            result += (
                f"<tr><td>Long Description</td><td>{self.long_description}</td></tr>"
            )
            result += f"<tr><td>Search Terms</td><td>{self.search_terms}</td></tr>"
            result += "</table>"
            return
        result += "<h3>Solution</h3>"
        result += f"<h4>Short Description</h4> <p>{self.short_description}</p>"
        result += f"<h4>Long Description</h4>" f"<p>{self.long_description}</p>"
        result += f"<h4>Search Terms</h4> <p>{self.search_terms}</p>"
        return result
