import datetime
import time
from typing import Annotated
from fastapi import Body, FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

import api.ollama as ollama

from data.helper import get_content_list

from my_db import Session
import models.models as db_models
from data.Solution import Solution
from data.types import Content
import data.apischema as apischema
from sqlalchemy import Date, cast

from task.worker import worker

from data.VulnerabilityReport import create_from_flama_json

from ai.LLM.Stretegies.OLLAMAService import OLLAMAService
from ai.LLM.LLMServiceStrategy import LLMServiceStrategy

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
        if ollama.is_up():
            ollama_health = "UP"
    except Exception as e:
        print(f"Error checking Ollama health, probably is down: {e}")

    system_info = {
        "status": "UP",  # pretty trivial since it did answer if you see this. Let's still include it for further use.
        "uptime": round(time.time() - start_time, 2),
        "external_modules": {"ollama": ollama_health},
    }
    return system_info, 200


@app.post("/upload")
async def upload(data: Annotated[apischema.StartRecommendationTaskRequest, Body(...)]):
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
        if existing_task and data.force_update is False:
            raise HTTPException(
                status_code=400, detail="Recommendation task already exists for today"
            )

        if data.force_update and existing_task:
            # Will nuke old task with all its findings.
            if existing_task.status == db_models.TaskStatus.PENDING:
                raise HTTPException(
                    status_code=400,
                    detail="Recommendation task is already processing, cannot exit",
                )

            s.query(db_models.RecommendationTask).filter(
                db_models.RecommendationTask.id == existing_task.id
            ).delete()
            s.commit()

        recommendation_task = db_models.RecommendationTask()

        s.add(recommendation_task)
        s.commit()
        s.flush()
        s.refresh(recommendation_task)
        for c in content_list:
            find = db_models.Finding().from_data(c)
            find.recommendation_task_id = recommendation_task.id
            s.add(find)
        s.commit()
        recommendation_task_id = recommendation_task.id
    # start subprocess for processing the data
    # ...

    worker.send_task("worker.generate_report", args=[recommendation_task_id])

    response = apischema.StartRecommendationTaskResponse(task_id=recommendation_task_id)

    return response


@app.get("/status")
def status():
    """
    This function returns the status of the recommendation task.
    :return: 200 OK with the status of the task.
    """
    with Session() as s:

        today = datetime.datetime.now().date()

        task = (
            s.query(db_models.RecommendationTask)
            .filter(cast(db_models.RecommendationTask.created_at, Date) == today)
            .first()
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return apischema.GetRecommendationTaskStatusResponse(status=task.status)


@app.get("/recommendations")
def recommendations(request: Annotated[apischema.GetRecommendationRequest, Body(...)]):
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """

    # get the findings
    # ...
    with Session() as s:
        total_count = s.query(db_models.Finding).count()

        findings = (
            s.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .where(
                db_models.RecommendationTask.status == db_models.TaskStatus.COMPLETED,
                cast(db_models.RecommendationTask.created_at, Date)
                == datetime.datetime.now().date(),
            )
            .offset(request.pagination.offset)
            .limit(request.pagination.limit)
            .all()
        )
        response = apischema.GetRecommendationResponse(
            items=[
                apischema.GetRecommendationResponseItem(
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
