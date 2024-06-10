import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import api.ollama as ollama
from data.helper import get_content_list
from data.types import Recommendation, Response
from db import Session
from models.models import Finding
from models.models import Recommendation as DBRecommendation

# from data.Findings import Findings


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
async def upload(request: Request):
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """

    json_data = await request.json()
    # Check if the JSON data is valid
    # TODO: fix required properties for eg cvss_rating_list is not required
    # if not validate_json(json_data):
    #     return 'Invalid JSON data', 400

    # Convert into Response object
    response = Response.validate(json_data)

    # get the content list
    content_list = get_content_list(response)

    with Session() as s:
        for c in content_list:
            find = Finding(finding=c.title_list[0].element, content=c.json())
            s.add(find)
        s.commit()
    # start subprocess for processing the data
    # ...

    return 'Data uploaded successfully', 200


@app.get('/recommendations')
def recommendations():
    """
    This function returns the recommendations from the data.
    :return: 200 OK with the recommendations or 204 NO CONTENT if there are no recommendations with retry-after header.
    """

    # get the findings
    # ...
    with Session() as s:
        recs = s.query(DBRecommendation).all()

    recommendations = [Recommendation(recommendation='aa', generic=True) for r in recs]
    # get the recommendations

    if recommendations:
        return recommendations, 200
    else:
        return 'No recommendations found', 204, {'Retry-After': 60}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
