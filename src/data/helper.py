from typing import List

from data.apischema import FindingInputFilter
from data.types import Content, InputData

# ##TODO:maybe using pydantic should be enough
# def validate_json(data: any) -> bool:
#     try:
#         json_data = data
#         try:
#             validate(instance=json_data, schema=schema)
#             print("JSON data adheres to the schema.")
#         except jsonschema.exceptions.ValidationError as e:
#             print("JSON data does not adhere to the schema.")
#             print(e)
#     except ValueError as e:
#         return False

#     return True


def get_content_list(json_data: InputData) -> list[Content]:
    return json_data.message.content

def filter_findings(findings: List[Content], filter: FindingInputFilter) -> List[Content]:
    def matches(content: Content) -> bool:
        if filter.source and not any(title.source in filter.source for title in content.title_list):
            return False

        if filter.severity and not (filter.severity[0] <= content.severity <= filter.severity[1]):
            return False

        if filter.priority and not (filter.priority[0] <= content.priority <= filter.priority[1]):
            return False

        if filter.cve_ids and not any(cve.element in filter.cve_ids for cve in content.cve_id_list):
            return False

        if filter.cwe_ids and not any(element in filter.cwe_ids for cwe in content.cwe_id_list or [] for element in cwe.element):
            return False
        return True

    return [content for content in findings if matches(content)]