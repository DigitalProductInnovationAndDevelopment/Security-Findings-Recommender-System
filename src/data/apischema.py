from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from data.AggregatedSolution import AggregatedSolution
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
    severity: Optional[SeverityFilter] = None  # ['low', 'high']
    priority: Optional[SeverityFilter] = None  # ['low', 'high']
    cve_ids: Optional[List[str]] = None
    cwe_ids: Optional[List[str]] = None
    source: Optional[List[str]] = None


class UploadPreference(BaseModel):
    long_description: Optional[bool] = Field(default=True)
    search_terms: Optional[bool] = Field(default=True)
    aggregated_solutions: Optional[bool] = Field(default=True)


class StartRecommendationTaskRequest(BaseModel):
    preferences: Optional[UploadPreference] = UploadPreference(
        long_description=True, search_terms=True, aggregated_solutions=True
    )
    data: InputData
    force_update: Optional[bool] = False
    filter: Optional[FindingInputFilter] = None


class StartRecommendationTaskResponse(BaseModel):
    task_id: int


class GetRecommendationFilter(BaseModel):
    task_id: Optional[int] = None
    date: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[SeverityFilter] = None  # ['low', 'high']
    cve_id: Optional[str] = None
    source: Optional[str] = None


class GetRecommendationRequest(BaseModel):
    user_id: Optional[int] = None
    filter: Optional[GetRecommendationFilter] = GetRecommendationFilter()
    pagination: Optional[PaginationInput] = PaginationInput(offset=0, limit=10)


class GetRecommendationResponseItem(Finding):
    pass

class GetRecommendationResponseItems(BaseModel):
    findings: list[GetRecommendationResponseItem]
    aggregated_solutions: list[GetRecommendationResponseItem]

class GetRecommendationResponse(BaseModel):
    items: GetRecommendationResponseItems
    pagination: Pagination


class GetRecommendationTaskStatusResponse(BaseModel):
    status: TaskStatus


class GetAggregatedRecommendationFilter(BaseModel):
    task_id: Optional[int] = None


class GetAggregatedRecommendationRequest(BaseModel):
    filter: Optional[GetAggregatedRecommendationFilter] = None


class GetAggregatedRecommendationResponseItem(AggregatedSolution):
    pass


class GetAggregatedRecommendationResponse(BaseModel):
    items: List[GetAggregatedRecommendationResponseItem]
