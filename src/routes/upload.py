from fastapi.routing import APIRouter
from fastapi.routing import APIRouter

import datetime
from typing import Annotated

from fastapi import Body, HTTPException
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
import data.apischema as apischema
import db.models as db_models
from data.helper import get_content_list
from fastapi import Depends
from db.my_db import get_db
from worker.worker import worker
from config import config

router = APIRouter(prefix="/upload")


@router.post("/")
async def upload(
    data: Annotated[apischema.StartRecommendationTaskRequest, Body(...)],
    db: Session = Depends(get_db),
) -> apischema.StartRecommendationTaskResponse:
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """
    # get the content list

    content_list = get_content_list(data.data)

    recommendation_task_id = None

    today = datetime.datetime.now().date()
    existing_task = (
        db.query(db_models.RecommendationTask)
        .filter(cast(db_models.RecommendationTask.created_at, Date) == today)
        .order_by(db_models.RecommendationTask.created_at)
        .first()
    )
    if existing_task and not data.force_update:
        raise HTTPException(
            status_code=400, detail="Recommendation task already exists for today"
        )

    if data.force_update and existing_task:
        # Will nuke old task with all its findingdb.
        if existing_task.status == db_models.TaskStatus.PENDING:
            print(config.redis_endpoint)
            revoked = worker.control.revoke(
                existing_task.celery_task_id, terminate=True
            )
            print(revoked)

            # pass

            # raise HTTPException(
            #     status_code=400,
            #     detail="Recommendation task is already processing, cannot exit",
            # )

        db.delete(existing_task)
        db.commit()
    recommendation_task = db_models.RecommendationTask()
    db.add(recommendation_task)
    db.commit()
    db.flush()
    db.refresh(recommendation_task)

    for c in content_list:
        find = db_models.Finding().from_data(c)
        find.recommendation_task_id = recommendation_task.id
        db.add(find)
    db.commit()

    celery_result = worker.send_task(
        "worker.generate_report", args=[recommendation_task.id]
    )

    recommendation_task.celery_task_id = celery_result.id
    db.commit()
    db.flush()

    recommendation_task_id = recommendation_task.id
    # start subprocess for processing the data
    # ...
    print("data", recommendation_task_id)
    response = apischema.StartRecommendationTaskResponse(task_id=recommendation_task_id)

    return response
