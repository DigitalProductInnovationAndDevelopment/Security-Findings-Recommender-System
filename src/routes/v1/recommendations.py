import datetime
from typing import Annotated

from fastapi import Body, Depends, HTTPException, Response
from fastapi.routing import APIRouter
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

import data.apischema as apischema
import db.models as db_models
from db.my_db import get_db
from dto.finding import db_finding_to_response_item
from repository.finding import get_finding_repository
from repository.task import TaskRepository, get_task_repository

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
    if severityFilter:
        findings = finding_repository.get_findings_by_task_id_and_severity(task.id, severityFilter, request.pagination)
    else:
        findings = finding_repository.get_findings_by_task_id(task.id, request.pagination)

    total_count = finding_repository.get_findings_count_by_task_id(task.id)
    
    response = apischema.GetRecommendationResponse(
        items=apischema.GetRecommendationResponseItems(
            findings= [db_finding_to_response_item(find) for find in findings],
            aggregated_solutions= []),
        pagination=apischema.Pagination(
            offset=request.pagination.offset,
            limit=request.pagination.limit,
            total=total_count,
            count=len(findings),
        ),
    )

    if not response or len(response.items.findings) == 0:
        return Response(status_code=204, headers={"Retry-After": "120"})

    return response
