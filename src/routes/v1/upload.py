import datetime
from typing import Annotated

from fastapi import Body, Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

import data.apischema as apischema
import db.models as db_models
from config import config
from data.helper import filter_findings, get_content_list
from db.my_db import get_db
from repository.finding import get_finding_repository
from repository.task import TaskRepository, get_task_repository
from worker.types import GenerateReportInput
from worker.worker import worker

router = APIRouter(prefix="/upload")


@router.post("/")
async def upload(
    data: Annotated[apischema.StartRecommendationTaskRequest, Body(...)],
    task_repository: TaskRepository = Depends(get_task_repository),
    finding_repository=Depends(get_finding_repository),
) -> apischema.StartRecommendationTaskResponse:
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """
    # get the content list

    content_list = get_content_list(data.data)
    if data.filter:
        content_list = filter_findings(content_list, data.filter)

    today = datetime.datetime.now().date()
    existing_task = task_repository.get_task_by_date(today)
    if existing_task and not data.force_update:
        raise HTTPException(
            status_code=400, detail="Recommendation task already exists for today"
        )

    if data.force_update and existing_task:
        # revoke the existing task
        if existing_task.status == db_models.TaskStatus.PENDING:
            worker.control.revoke(existing_task.celery_task_id, terminate=True)

        task_repository.delete_task(existing_task)

    # create a new task
    recommendation_task = task_repository.create_task()

    findings = []
    for c in content_list:
        find = db_models.Finding().from_data(c)
        find.recommendation_task_id = recommendation_task.id
        findings.append(find)
    finding_repository.create_findings(findings)
    worker_input = GenerateReportInput(
        recommendation_task_id=recommendation_task.id,
        generate_long_solution=data.preferences.long_description,
        generate_search_terms=data.preferences.search_terms,
        generate_aggregate_solutions=data.preferences.aggregated_solutions,
    )

    celery_result = worker.send_task(
        "worker.generate_report",
        args=[worker_input.model_dump()],
    )

    # update the task with the celery task id
    task_repository.update_task(recommendation_task, celery_result.id)

    response = apischema.StartRecommendationTaskResponse(task_id=recommendation_task.id)
    return response
