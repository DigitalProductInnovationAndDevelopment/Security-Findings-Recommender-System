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


from repository.task import TaskRepository, get_task_repository

router = APIRouter(
    prefix="/tasks",
)


@router.get("/")
def tasks(task_repository: TaskRepository = Depends(get_task_repository)):
    """
    This function returns all the tasks.
    :return: 200 OK with the tasks.
    """
    tasks = task_repository.get_tasks()

    return tasks


@router.delete("/{task_id}")
def delete_task(
    task_id: int, task_repository: TaskRepository = Depends(get_task_repository)
):
    """
    This function deletes the task.
    :return: 200 OK with the tasks.
    """

    task = task_repository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status == db_models.TaskStatus.PENDING:
        if task.celery_task_id:
            worker.control.revoke(task.celery_task_id, terminate=True)
    task_repository.delete_task(task)
    return task


@router.delete("/")
def delete_tasks(task_repository: TaskRepository = Depends(get_task_repository)):
    """
    This function deletes all the tasks.
    :return: 200 OK with the tasks.
    """

    count = task_repository.delete_all_tasks()
    task_repository.session.flush()

    return "Deleted {} tasks".format(count)


@router.get("/{task_id}/status")
def status(
    task_id: int,
    task_repository: TaskRepository = Depends(get_task_repository),
) -> apischema.GetRecommendationTaskStatusResponse:
    """
    This function returns the status of the recommendation task.
    :return: 200 OK with the status of the task.
    """

    task = task_repository.get_task_by_id(task_id)

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
