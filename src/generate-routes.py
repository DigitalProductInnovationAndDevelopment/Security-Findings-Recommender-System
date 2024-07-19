# generate_routes.py

from fastapi import FastAPI
import os

# Import your FastAPI app here
from app import app


def generate_routes(app: FastAPI):
    output = []
    for route in app.routes:
        methods = ", ".join(route.methods)
        output.append(f"{methods} {route.path}")
    return "\n".join(output)


if __name__ == "__main__":
    routes = generate_routes(app)
    with open("api_routes.txt", "w") as file:
        file.write(routes)
    print("API routes generated and saved to api_routes.txt")
