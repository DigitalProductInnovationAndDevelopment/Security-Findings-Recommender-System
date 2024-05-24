from flask import Flask, request
import time

from src.data.Findings import Findings
from src.data.types import Response
from src.data.helper import validate_json, get_content_list

import src.api.ollama as ollama

app = Flask(__name__)

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
def upload():
    """
    This function takes the string from the request and converts it to a data object.
    :return: 200 OK if the data is valid, 400 BAD REQUEST otherwise.
    """
    json_data = request.get_json()
    # Check if the JSON data is valid
    if not validate_json(json_data):
        return 'Invalid JSON data', 400

    # Convert into Response object
    response = Response(**json_data)

    # get the content list
    content_list = get_content_list(response)

    findings = Findings(content_list)

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

    # get the recommendations
    recommendations = None

    if recommendations:
        return recommendations, 200
    else:
        return 'No recommendations found', 204, {'Retry-After': 60}


if __name__ == '__main__':
    app.run(debug=True)
