class Solution:
    def __init__(
        self,
        short_description: str = None,
        long_description: str = None,
        search_terms: list = None,
    ):
        self.short_description = short_description
        self.long_description = long_description
        self.search_terms = search_terms
        self.metadata = {}

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
            "search_terms": self.search_terms if self.search_terms is not None else [],
            "metadata": self.metadata,
        }

    def __str__(self):
        result = ""
        result += "-------    Solution    -------\n"
        result += f"Short Description: {self.short_description}\n"
        result += f"Long Description: {self.long_description}\n"
        result += f"Search Terms: {self.search_terms}\n"
        return result

    def to_html(self, table=False):
        result = ""
        result += "<h3>Solution</h3>"
        result += f"<h4>Short Description</h4> <p>{self.short_description}</p>"
        if table:
            result += (
                f"<h4>Long Description</h4><table style='width:100%'>"
                + "<thead><tr><th align='left'>Step</th><th text-"
                "align='left'>Description</th></tr></thead>"
                + "".join(
                    [
                        f"<tr><td align='left'>{x[0] + 1}</td><td text-align='left'><p>{x[1]}</p></td></tr>"
                        for x in enumerate(self.long_description)
                    ]
                )
                + "</table>"
            )
        else:
            result += f"<h4>Long Description</h4><ul>{''.join([f'<li>{x}</li>' for x in self.long_description])}</ul>"
        result += f"<h4>Search Terms</h4> <p>{self.search_terms}</p>"
        return result
