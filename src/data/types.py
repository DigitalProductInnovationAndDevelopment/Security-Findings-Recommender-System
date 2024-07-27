from typing import List, Dict, Any, Union, Optional
from typing import Any, Optional, Tuple

from typing_extensions import Annotated

from pydantic import BaseModel


# deprecated
schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "message": {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "utc_age": {"type": "string"},
                "content": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "doc_type": {"type": "string"},
                            "criticality_tag": {"type": ["array", "object"]},
                            "knowledge_type": {"type": "string"},
                            "requirement_list": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "title_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "location_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "description_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "internal_rating_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "internal_ratingsource_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "cvss_rating_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "rule_list": {"type": "array", "items": {"type": "object"}},
                            "cwe_id_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "cve_id_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "activity_list": {
                                "type": "array",
                                "items": {"type": "object"},
                            },
                            "first_found": {"type": "string"},
                            "last_found": {"type": "string"},
                            "report_amount": {"type": "integer"},
                            "content_hash": {"type": "string"},
                            "severity": {"type": "integer"},
                            "severity_explanation": {"type": "string"},
                            "priority": {"type": "integer"},
                            "priority_explanation": {"type": "string"},
                            "sum_id": {"type": "string"},
                            "prio_id": {"type": "string"},
                            "element_tag": {"type": "string"},
                        },
                        "required": [
                            "doc_type",
                            "criticality_tag",
                            "knowledge_type",
                            "requirement_list",
                            "title_list",
                            "location_list",
                            "description_list",
                            "internal_rating_list",
                            "internal_ratingsource_list",
                            "cvss_rating_list",
                            "rule_list",
                            "cwe_id_list",
                            "cve_id_list",
                            "activity_list",
                            "first_found",
                            "last_found",
                            "report_amount",
                            "content_hash",
                            "severity",
                            "severity_explanation",
                            "priority",
                            "priority_explanation",
                            "sum_id",
                            "prio_id",
                            "element_tag",
                        ],
                    },
                },
            },
            "required": ["version", "utc_age", "content"],
        },
    },
    "required": ["status", "message"],
}


class Tag(BaseModel):
    action: str
    user_mail: str
    action_reason: str
    created_at: str
    valid_until: str


class Location(BaseModel):
    location: str
    amount: int
    source: str
    last_found: str
    first_found: str
    tags: List[Tag]


class Title(BaseModel):
    element: str
    source: str


class Description(BaseModel):
    element: str
    source: str


class Rating(BaseModel):
    element: str
    source: str


class CvssRating(BaseModel):
    element: str
    source: str


class Rule(BaseModel):
    element: str
    source: str


class CveId(BaseModel):
    element: str
    source: str


class CweId(BaseModel):
    element: List[str]
    source: str


class Activity(BaseModel):
    element: str
    source: str


class Content(BaseModel):
    doc_type: str
    criticality_tag: Union[List[Union[str, int]], Dict[str, Any]]
    knowledge_type: str
    requirement_list: List[str]
    title_list: List[Title]
    location_list: List[Location]
    description_list: Optional[List[Description]] = []
    internal_rating_list: Optional[List[Rating]] = []
    internal_ratingsource_list: List[Rating]
    cvss_rating_list: Optional[List[CvssRating]] = []
    rule_list: List[Rule]
    cve_id_list: Optional[List[CveId]] = []
    cwe_id_list: Optional[List[CweId]] = []
    activity_list: List[Activity]
    first_found: str
    last_found: str
    report_amount: int
    content_hash: str
    severity: int
    severity_explanation: str
    priority: int
    priority_explanation: str
    sum_id: str
    prio_id: str
    element_tag: str


class Message(BaseModel):
    version: str
    utc_age: str
    content: List[Content]


class InputData(BaseModel):
    status: str
    message: Message


class Finding(BaseModel):
    content: Content
    solutions: List[Dict[str, Any]] = []


class Recommendation(BaseModel):
    recommendation: str
    generic: bool
