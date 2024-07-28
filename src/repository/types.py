from typing import Optional
from pydantic import BaseModel

from data.AggregatedSolution import AggregatedSolution
from data.apischema import SeverityFilter
from data.pagination import PaginationInput


class AggregatedSolutionInput(BaseModel):
    solution: AggregatedSolution
    findings_db_ids: list[int]


class CreateAggregatedRecommendationInput(BaseModel):
    aggregated_solutions: list[AggregatedSolutionInput]
    recommendation_task_id: int


class GetFindingsByFilterInput(BaseModel):
    task_id: int
    severityFilter: Optional[SeverityFilter] = None
    pagination: Optional[PaginationInput] = None
