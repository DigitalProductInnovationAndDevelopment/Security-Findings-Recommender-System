from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, validator

from data.Categories import Category
from data.Finding import Finding
from data.pagination import Pagination, PaginationInput
from data.Solution import Solution
from data.types import InputData
from db.models import TaskStatus


class SeverityFilter(BaseModel):
    minValue: int
    maxValue: int
class FindingInputFilter(BaseModel):
    severity: Optional[SeverityFilter] = None # ['low', 'high']
    priority: Optional[SeverityFilter] = None # ['low', 'high']
    cve_ids: Optional[List[str]] = None
    cwe_ids: Optional[List[str]] = None
    source: Optional[List[str]] = None
    
class StartRecommendationTaskRequest(BaseModel):
    user_id: Optional[int] = None
    strategy: Optional[Literal["OLLAMA", "ANTHROPIC", "OPENAI"]] = "OLLAMA"
    data: InputData
    force_update: Optional[bool] = False
    filter: Optional[FindingInputFilter] = None


class StartRecommendationTaskResponse(BaseModel):
    task_id: int


class GetRecommendationFilter(BaseModel):
    task_id: Optional[int] = None
    date: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[SeverityFilter] = None # ['low', 'high']
    cve_id: Optional[str] = None
    source: Optional[str] = None


class GetRecommendationRequest(BaseModel):
    user_id: Optional[int] = None
    filter: Optional[GetRecommendationFilter] = GetRecommendationFilter()
    pagination: Optional[PaginationInput] = PaginationInput(offset=0, limit=10)


class SolutionItem(BaseModel):
    short_description: str
    long_description: str
    metadata: dict
    search_terms: str


class GetRecommendationResponseItem(Finding):  # TODO adapt needed fields
    pass


class GetRecommendationResponse(BaseModel):
    items: list[GetRecommendationResponseItem]
    pagination: Pagination


class GetRecommendationTaskStatusResponse(BaseModel):
    status: TaskStatus


class GetSummarizedRecommendationRequest(BaseModel):
    user_id: Optional[int]
    pagination: PaginationInput = PaginationInput(offset=0, limit=10)


# class GetSummarizedRecommendationResponse(BaseModel):
#     recommendation: list[Recommendation]
#     pagination: Pagination
