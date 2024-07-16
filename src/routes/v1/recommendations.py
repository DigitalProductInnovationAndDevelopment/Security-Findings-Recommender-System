from fastapi.routing import APIRouter

import datetime
from typing import Annotated

from fastapi import Body, HTTPException, Response
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from fastapi import Depends
from db.my_db import get_db
import data.apischema as apischema
import db.models as db_models
from data.Finding import FindingKind
from data.Solution import Solution
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

    findings = finding_repository.get_findings_by_task_id(task.id, request.pagination)

    total_count = finding_repository.get_findings_count_by_task_id(task.id)

    response = apischema.GetRecommendationResponse(
        items=[db_finding_to_response_item(find) for find in findings],
        pagination=apischema.Pagination(
            offset=request.pagination.offset,
            limit=request.pagination.limit,
            total=total_count,
            count=len(findings),
        ),
    )

    if not response or len(response.items) == 0:
        return Response(status_code=204, headers={"Retry-After": "120"})

    return response
