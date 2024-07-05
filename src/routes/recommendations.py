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

router = APIRouter(
    prefix="/recommendations",
)


@router.post("/")
def recommendations(
    request: Annotated[apischema.GetRecommendationRequest, Body(...)],
    db: Session = Depends(get_db),
) -> apischema.GetRecommendationResponse:
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """
    task_id = request.filter.task_id if request.filter else None
    # get the findings
    # ...

    total_count = db.query(db_models.Finding).count()
    today = datetime.datetime.now().date()
    task = (
        db.query(db_models.RecommendationTask)
        .filter(
            db_models.RecommendationTask.id == task_id
            if task_id
            else cast(db_models.RecommendationTask.created_at, Date) == today
        )
        .first()
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

    findings = (
        db.query(db_models.Finding)
        .join(db_models.RecommendationTask)
        .where(
            db_models.RecommendationTask.status == db_models.TaskStatus.COMPLETED,
            (
                db_models.RecommendationTask.id == task_id
                if task_id
                else cast(db_models.RecommendationTask.created_at, Date) == today
            ),
        )
        .offset(request.pagination.offset)
        .limit(request.pagination.limit)
        .all()
    )
    response = apischema.GetRecommendationResponse(
        items=[
            apischema.GetRecommendationResponseItem(
                category=(
                    FindingKind[find.recommendations[0].category]
                    if find.recommendations
                    else FindingKind.DEFAULT
                ),
                solution=Solution(
                    short_description=(
                        find.recommendations[0].description_short
                        if find.recommendations
                        else None
                    ),
                    long_description=(
                        find.recommendations[0].description_long
                        if find.recommendations
                        else None
                    ),
                    search_terms=(
                        find.recommendations[0].search_terms
                        if find.recommendations
                        else None
                    ),
                    metadata=(
                        find.recommendations[0].meta if find.recommendations else {}
                    ),
                ),
            ).from_json(find.raw_data)
            for find in findings
        ],
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
