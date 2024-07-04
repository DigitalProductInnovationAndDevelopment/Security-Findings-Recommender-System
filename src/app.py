import datetime
import os
import time
from typing import Annotated, Optional

from fastapi import Body, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Date, cast

import ai.LLM.Stretegies.OLLAMAService
import data.apischema as apischema
import models.models as db_models
from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
from ai.LLM.Stretegies.OLLAMAService import OLLAMAService
from data.Finding import FindingKind
from data.helper import get_content_list
from data.Solution import Solution
from data.types import Content
from data.VulnerabilityReport import create_from_flama_json
from my_db import Session, get_db_url
from task.worker import worker
from config import settings


my_strategy = OLLAMAService()
llm_service = LLMServiceStrategy(my_strategy)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start_time = time.time()


@app.get("/")
def health():
    # check ollama health
    ollama_health = "DOWN"
    try:
        if ai.LLM.Stretegies.OLLAMAService.is_up():
            ollama_health = "UP"
    except Exception as e:
        print(f"Error checking Ollama health, probably is down: {e}")

    system_info = {
        "status": "UP",  # pretty trivial since it did answer if you see this. Let's still include it for further use.
        "uptime": round(time.time() - start_time, 2),
        "external_modules": {"ollama": ollama_health},
        "urls": {
            "llm": llm_service.get_url(),
            "redis": os.getenv("REDIS_ENDPOINT"),
            # this leaks the db user and password in dev mode
            "postgres": (
                get_db_url()
                if os.getenv("ENVIRONMENT") == "development"
                else "retracted"
            ),
        },
    }
    return system_info


@app.post("/upload")
async def upload(
    data: Annotated[apischema.StartRecommendationTaskRequest, Body(...)]
) -> apischema.StartRecommendationTaskResponse:
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """
    # get the content list

    content_list = get_content_list(data.data)

    data2 = [x.dict() for x in content_list]
    vulnerability_report = create_from_flama_json(data2, n=5, llm_service=llm_service)
    print(vulnerability_report.findings[0].llm_service)
    recommendation_task_id = None
    with Session() as s:
        today = datetime.datetime.now().date()
        existing_task = (
            s.query(db_models.RecommendationTask)
            .filter(cast(db_models.RecommendationTask.created_at, Date) == today)
            .order_by(db_models.RecommendationTask.created_at)
            .first()
        )
        if existing_task and not data.force_update:
            raise HTTPException(
                status_code=400, detail="Recommendation task already exists for today"
            )

        if data.force_update and existing_task:
            # Will nuke old task with all its findings.
            if existing_task.status == db_models.TaskStatus.PENDING:
                revoked = worker.control.revoke(
                    existing_task.celery_task_id, terminate=True
                )
                print(revoked)

                # pass

                # raise HTTPException(
                #     status_code=400,
                #     detail="Recommendation task is already processing, cannot exit",
                # )

            s.query(db_models.RecommendationTask).filter(
                db_models.RecommendationTask.id == existing_task.id
            ).delete()
            s.commit()

        recommendation_task = db_models.RecommendationTask()
        s.add(recommendation_task)
        s.commit()
        s.flush()
        s.refresh(recommendation_task)
        celery_result = worker.send_task(
            "worker.generate_report", args=[recommendation_task.id]
        )
        print("taskid", celery_result.id)
        print(celery_result)
        recommendation_task.celery_task_id = celery_result.id
        s.commit()
        s.flush()
        for c in content_list:
            find = db_models.Finding().from_data(c)
            find.recommendation_task_id = recommendation_task.id
            s.add(find)
        s.commit()
        recommendation_task_id = recommendation_task.id
    # start subprocess for processing the data
    # ...

    response = apischema.StartRecommendationTaskResponse(task_id=recommendation_task_id)

    return response


@app.get("/status")
def status(
    task_id: Optional[int] = None,
) -> apischema.GetRecommendationTaskStatusResponse:
    """
    This function returns the status of the recommendation task.
    :return: 200 OK with the status of the task.
    """
    with Session() as s:
        today = datetime.datetime.now().date()

        task = (
            s.query(db_models.RecommendationTask)
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


@app.get("/tasks")
def tasks():
    """
    This function returns all the tasks.
    :return: 200 OK with the tasks.
    """
    with Session() as s:
        tasks = s.query(db_models.RecommendationTask).all()
        return tasks


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    This function deletes the task.
    :return: 200 OK with the tasks.
    """
    with Session() as s:
        task = (
            s.query(db_models.RecommendationTask)
            .filter(db_models.RecommendationTask.id == task_id)
            .first()
        )
        print(task)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status == db_models.TaskStatus.PENDING:
            worker.control.revoke(task.celery_task_id, terminate=True)

        s.delete(task)
        s.commit()
        return task


@app.delete("/tasks")
def delete_tasks():
    """
    This function deletes all the tasks.
    :return: 200 OK with the tasks.
    """
    with Session() as s:
        s.query(db_models.RecommendationTask).delete()
        s.commit()
        return "All tasks deleted"


@app.post("/recommendations")
def recommendations(
    request: Annotated[apischema.GetRecommendationRequest, Body(...)]
) -> apischema.GetRecommendationResponse:
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """
    task_id = request.filter.task_id if request.filter else None
    # get the findings
    # ...
    with Session() as s:
        total_count = s.query(db_models.Finding).count()
        today = datetime.datetime.now().date()
        task = (
            s.query(db_models.RecommendationTask)
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
            s.query(db_models.Finding)
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
