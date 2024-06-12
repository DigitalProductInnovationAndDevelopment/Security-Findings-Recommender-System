from pydantic import BaseModel
from typing import Optional

from data.pagination import Pagination, PaginationInput
from data.types import Recommendation, InputData, Content


class StartRecommendationTaskRequest(BaseModel):
    user_id: int
    data: InputData
    force_update: Optional[bool] = False


class StartRecommendationTaskResponse(BaseModel):
    task_id: int


class GetRecommendationFilter(BaseModel):
    location: Optional[str]
    severity: Optional[str]
    cve_id: Optional[str]
    source: Optional[str]


class GetRecommendationRequest(BaseModel):
    user_id: Optional[int]
    filter: Optional[GetRecommendationFilter]
    pagination: Optional[PaginationInput] = PaginationInput(offset=0, limit=10)


class GetRecommendationResponseItem(BaseModel):  # TODO adapt needed fields
    description_short: str
    description_long: str
    search_terms: str
    meta: dict
    finding: Content


class GetRecommendationResponse(BaseModel):
    items: list[GetRecommendationResponseItem]
    pagination: Pagination


class GetSummarizedRecommendationRequest(BaseModel):
    user_id: Optional[int]
    pagination: PaginationInput = PaginationInput(offset=0, limit=10)


class GetSummarizedRecommendationResponse(BaseModel):
    recommendation: list[Recommendation]
    pagination: Pagination
