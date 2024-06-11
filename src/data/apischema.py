



from pydantic import BaseModel
from typing import Optional

from data.pagination import Pagination,PaginationInput
from data.types import Recommendation, Content,Response


class StartRecommendationTaskRequest(BaseModel):
    user_id: int
    data: Response
    force_update: Optional[bool] = False
    
class StartRecommendationTaskResponse(BaseModel):
    task_id: int


class GetRecommendationFilter(BaseModel):
    location:Optional[str]
    severity: Optional[str]
    cve_id: Optional[str]
    source: Optional[str]


class GetRecommendationRequest(BaseModel):
    user_id: int
    filter:  Optional[GetRecommendationFilter]
    pagination: Optional[PaginationInput] = PaginationInput(offset=0, limit=10)
    

    
class GetRecommendationResponseItem(BaseModel):
    description_short: str
    description_long: str
    finding: str
    
class GetRecommendationResponse(BaseModel):
    items:  list[GetRecommendationResponseItem]
    pagination: Pagination
    
    
class GetSummarizedRecommendationRequest(BaseModel):
    user_id: int
    pagination: PaginationInput = PaginationInput(offset=0, limit=10)
    

class GetSummarizedRecommendationResponse(BaseModel):
    recommendation: list[Recommendation]
    pagination: Pagination
    
    
