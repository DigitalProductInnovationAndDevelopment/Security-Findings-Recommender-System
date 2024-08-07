import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import ai.LLM.Strategies.OLLAMAService
from config import config


import routes
import routes.v1.recommendations
import routes.v1.task
import routes.v1.upload


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes.v1.task.router, prefix="/api/v1")
app.include_router(routes.v1.recommendations.router, prefix="/api/v1")
app.include_router(routes.v1.upload.router, prefix="/api/v1")

start_time = time.time()


@app.get("/")
def health():
    # check ollama health
    ollama_health = "DOWN"
    try:
        if ai.LLM.Strategies.OLLAMAService.is_up():
            ollama_health = "UP"
    except Exception as e:
        print(f"Error checking Ollama health, probably is down: {e}")

    system_info = {
        "status": "UP",  # pretty trivial since it did answer if you see this. Let's still include it for further use.
        "uptime": round(time.time() - start_time, 2),
        "external_modules": {"ollama": ollama_health},
        "urls": {
            "redis": (
                config.redis_endpoint
                if config.environment == "development"
                else "retracted"
            ),
            # this leaks the db user and password in dev mode
            "postgres": (
                config.get_db_url()
                if config.environment == "development"
                else "retracted"
            ),
        },
    }
    return system_info
