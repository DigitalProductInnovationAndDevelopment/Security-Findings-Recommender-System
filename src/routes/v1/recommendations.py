import datetime
from typing import Annotated, Optional

from fastapi import Body, Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

import data.apischema as apischema
import db.models as db_models
from db.my_db import get_db
from dto.finding import db_finding_to_response_item
from repository.finding import get_finding_repository
from repository.recommendation import (
    RecommendationRepository,
    get_recommendation_repository,
)
from repository.task import TaskRepository, get_task_repository
from repository.types import GetFindingsByFilterInput

router = APIRouter(
    prefix="/recommendations",
)


@router.post("/")
def recommendations(
    request: Annotated[apischema.GetRecommendationRequest, Body(...)],
    db: Session = Depends(get_db),
    task_repository: TaskRepository = Depends(get_task_repository),
    finding_repository=Depends(get_finding_repository),
) -> apischema.GetRecommendationResponse:
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """
    task_id = request.filter.task_id if request.filter else None
    severityFilter = request.filter.severity if request.filter.severity else None
    # get the findings
    # ...

    today = datetime.datetime.now().date()

    task = (
        task_repository.get_task_by_id(task_id)
        if task_id
        else task_repository.get_task_by_date(today)
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail=(
                "Task for today not found"
                if not task_id
                else f"Task with id {task_id} not found"
            ),
        )

    if task.status == db_models.TaskStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Recommendation task is still processing",
        )

    if task.status == db_models.TaskStatus.FAILED:
        raise HTTPException(
            status_code=400,
            detail="Recommendation task failed",
        )
    findings, total = finding_repository.get_findings_by_task_id_and_filter(
        GetFindingsByFilterInput(
            task_id=task.id,
            severityFilter=severityFilter if severityFilter else None,
            pagination=request.pagination,
        )
    )

    response = apischema.GetRecommendationResponse(
        items=[db_finding_to_response_item(find) for find in findings],
        pagination=apischema.Pagination(
            offset=request.pagination.offset,
            limit=request.pagination.limit,
            total=total,
            count=len(findings),
        ),
    )
    return response


@router.post("/aggregated")
def aggregated_solutions(
    request: Annotated[
        Optional[apischema.GetAggregatedRecommendationRequest], Body(...)
    ],
    task_repository: TaskRepository = Depends(get_task_repository),
    recommendation_repository: RecommendationRepository = (
        Depends(get_recommendation_repository)
    ),
) -> apischema.GetAggregatedRecommendationResponse:

    today = datetime.datetime.now().date()
    task = None
    if request.filter and request.filter.task_id:
        task = task_repository.get_task_by_id(request.filter.task_id)
    else:
        task = task_repository.get_task_by_date(today)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Task with id {request.filter.task_id} not found"
                if request.filter and request.filter.task_id
                else "Task for today not found"
            ),
        )
    if task.status != db_models.TaskStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Recommendation status:" + task.status.value,
        )
    agg_recs = recommendation_repository.get_aggregated_solutions(task.id)
    return apischema.GetAggregatedRecommendationResponse(
        items=[
            apischema.GetAggregatedRecommendationResponseItem(
                solution=rec.solution,
                findings=[db_finding_to_response_item(x) for x in rec.findings],
                metadata=rec.meta,
            )
            for rec in agg_recs
        ]
    )
