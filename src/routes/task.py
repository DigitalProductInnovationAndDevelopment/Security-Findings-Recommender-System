from fastapi.routing import APIRouter
from fastapi import Depends
from db.my_db import get_db
from sqlalchemy.orm import Session
from worker.worker import worker

import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import Date, cast

import data.apischema as apischema
import db.models as db_models


router = APIRouter(
    prefix="/tasks",
)


@router.get("/")
def tasks(db: Session = Depends(get_db)):
    """
    This function returns all the tasks.
    :return: 200 OK with the tasks.
    """
    tasks = db.query(db_models.RecommendationTask).all()

    return tasks


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    This function deletes the task.
    :return: 200 OK with the tasks.
    """

    task = (
        db.query(db_models.RecommendationTask)
        .filter(db_models.RecommendationTask.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status == db_models.TaskStatus.PENDING:
        if task.celery_task_id:
            worker.control.revoke(task.celery_task_id, terminate=True)
    db.delete(task)
    db.commit()
    return task


@router.delete("/")
def delete_tasks(db: Session = Depends(get_db)):
    """
    This function deletes all the tasks.
    :return: 200 OK with the tasks.
    """

    db.query(db_models.RecommendationTask).delete()
    db.commit()
    return "All tasks deleted"


@router.get("/{task_id}/status")
def status(
    task_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> apischema.GetRecommendationTaskStatusResponse:
    """
    This function returns the status of the recommendation task.
    :return: 200 OK with the status of the task.
    """

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

    return apischema.GetRecommendationTaskStatusResponse(status=task.status)
