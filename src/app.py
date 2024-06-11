import datetime
import time
from typing import Annotated
from fastapi import Body, FastAPI,Response,Query
from fastapi.middleware.cors import CORSMiddleware

import api.ollama as ollama
from data.helper import get_content_list
from data.types import Recommendation, Response,Content
from my_db import Session
import models.models as db_models


import data.apischema as apischema

from sqlalchemy import Date, cast

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

start_time = time.time()


@app.get('/')
def health():
    # check ollama health
    ollama_health = "DOWN"
    try:
        if ollama.is_up():
            ollama_health = "UP"
    except Exception as e:
        print(f"Error checking Ollama health, probably is down: {e}")

    system_info = {
        'status': 'UP',  # pretty trivial since it did answer if you see this. Let's still include it for further use.
        'uptime': round(time.time() - start_time, 2),
        'external_modules': {
            'ollama': ollama_health
        }
    }
    return system_info, 200


@app.post('/upload')
async def upload(data: Annotated[apischema.StartRecommendationTaskRequest,Body(...)]):
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """

    # get the content list
    content_list = get_content_list(data.data)

    with Session() as s:
            today = datetime.datetime.now().date()
            existing_task = s.query(db_models.RecommendationTask).filter(cast(db_models.RecommendationTask.created_at,Date)== today).order_by(db_models.RecommendationTask.created_at).first()
            if existing_task and data.force_update is False:
                
                return 'Recommendation task already exists for today', 400
            
            if(data.force_update):
                # Will nuke old task with all its findings.
                if(existing_task.status == db_models.TaskStatus.PENDING):
                    return 'Recommendation task is already processing, cannot exit', 400
                
                s.query(db_models.RecommendationTask).filter(db_models.RecommendationTask.id == existing_task.id).delete()
                s.commit()
                s.delete(existing_task)
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
    # start subprocess for processing the data
    # ...

    return 'Data uploaded successfully'


@app.get('/recommendations')
def recommendations(request: Annotated[apischema.GetRecommendationRequest,Query(...)]):
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """

    # get the findings
    # ...
    with Session() as s:
        total_count = s.query(db_models.Finding).count()
        recs = s.query(db_models.Finding).join(db_models.RecommendationTask).offset(request.pagination.offset).limit(request.pagination.limit).all()
        findings = apischema.GetRecommendationResponse(
            items=[apischema.GetRecommendationResponseItem(
                description_short="this is a short description",
                description_long="this is a long description",
                finding='finding'
                
            ) for r in recs],
        pagination=apischema.Pagination(offset=request.pagination.offset, limit=request.pagination.limit,total=total_count )
        )
    
    if findings:
        return findings, 200
    else:
        return 'No recommendations found', 204, {'Retry-After': 60}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
