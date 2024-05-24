from dotenv import load_dotenv
import requests
import os

load_dotenv()  # take environment variables from .env. (This is only needed when not using docker-compose)


def prompt(prompt: str) -> str:
    ollama_url = os.getenv('OLLAMA_URL') + '/api/generate'
    if not ollama_url:
        raise ValueError('OLLAMA_URL not set in environment variables')

    ollama_model = os.getenv('OLLAMA_MODEL', 'llama3')  # default model is llama3, but can be changed in .env

    response = requests.post(f'{ollama_url}', json={'prompt': prompt, 'model': ollama_model, 'stream': False})
    data = response.json()
    try:
        return data['response']
    except KeyError:
        raise ValueError('Response from Ollama is not as expected')


def is_up() -> bool:
    res = requests.post(os.getenv('OLLAMA_URL') + '/api/show', json={'name': os.getenv('OLLAMA_MODEL', 'llama3')})
    if res.status_code ==200:
        return True
    else:
        return False
