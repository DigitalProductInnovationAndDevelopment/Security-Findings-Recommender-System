from pydantic import BaseModel
from typing import Optional, Literal

from data.pagination import Pagination, PaginationInput
from data.types import InputData
from data.Finding import Finding
from db.models import TaskStatus


class StartRecommendationTaskRequest(BaseModel):
    user_id: Optional[int] = None
    strategy: Optional[Literal["OLLAMA", "ANTHROPIC", "OPENAI"]] = "OLLAMA"
    data: InputData
    force_update: Optional[bool] = False


class StartRecommendationTaskResponse(BaseModel):
    task_id: int


class GetRecommendationFilter(BaseModel):
    task_id: Optional[int] = None
    date: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[str] = None
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
