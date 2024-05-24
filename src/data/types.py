from typing import List, Dict, Any, Union
from dataclasses import dataclass, field

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
                            "requirement_list": {"type": "array", "items": {"type": "string"}},
                            "title_list": {"type": "array", "items": {"type": "object"}},
                            "location_list": {"type": "array", "items": {"type": "object"}},
                            "description_list": {"type": "array", "items": {"type": "object"}},
                            "internal_rating_list": {"type": "array", "items": {"type": "object"}},
                            "internal_ratingsource_list": {"type": "array", "items": {"type": "object"}},
                            "cvss_rating_list": {"type": "array", "items": {"type": "object"}},
                            "rule_list": {"type": "array", "items": {"type": "object"}},
                            "cwe_id_list": {"type": "array", "items": {"type": "object"}},
                            "cve_id_list": {"type": "array", "items": {"type": "object"}},
                            "activity_list": {"type": "array", "items": {"type": "object"}},
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
                            "element_tag": {"type": "string"}
                        },
                        "required": ["doc_type", "criticality_tag", "knowledge_type", "requirement_list", "title_list",
                                     "location_list", "description_list", "internal_rating_list",
                                     "internal_ratingsource_list", "cvss_rating_list", "rule_list",
                                     "cwe_id_list", "cve_id_list", "activity_list", "first_found", "last_found",
                                     "report_amount", "content_hash", "severity", "severity_explanation",
                                     "priority", "priority_explanation", "sum_id", "prio_id", "element_tag"]
                    }
                }
            },
            "required": ["version", "utc_age", "content"]
        }
    },
    "required": ["status", "message"]
}


@dataclass
class Tag:
    action: str
    user_mail: str
    action_reason: str
    created_at: str
    valid_until: str


@dataclass
class Location:
    location: str
    amount: int
    source: str
    last_found: str
    first_found: str
    tags: List[Tag]


@dataclass
class Title:
    element: str
    source: str


@dataclass
class Description:
    element: str
    source: str


@dataclass
class Rating:
    element: str
    source: str


@dataclass
class CvssRating:
    element: str
    source: str


@dataclass
class Rule:
    element: str
    source: str


@dataclass
class CveId:
    element: str
    source: str


@dataclass
class Activity:
    element: str
    source: str


@dataclass
class Content:
    doc_type: str
    criticality_tag: Union[List[Union[str, int]], Dict[str, Any]]
    knowledge_type: str
    requirement_list: List[str]
    title_list: List[Title]
    location_list: List[Location]
    description_list: List[Description]
    internal_rating_list: List[Rating]
    internal_ratingsource_list: List[Rating]
    cvss_rating_list: List[CvssRating]
    rule_list: List[Rule]
    cwe_id_list: List[Dict[str, Any]]
    cve_id_list: List[CveId]
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


@dataclass
class Message:
    version: str
    utc_age: str
    content: List[Content]


@dataclass
class Response:
    status: str
    message: Message


@dataclass
class Finding:
    content: Content
    solutions: List[Dict[str, Any]] = field(default_factory=list)