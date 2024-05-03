# Security-Findings-Recommender-System

## Introduction
to be written

## Pre-requisites

### Docker
To run the code within Docker, you should install Docker Desktop from [the official website](https://www.docker.com/products/docker-desktop).

### Local / Development
To run the code without Docker, follow these steps:
- Install Python 3.8 or higher from [the official website](https://www.python.org/downloads/).
- Install the required packages by running the following command:
```bash
pip install -r requirements.txt
```

Optional: Create a virtual environment to isolate the dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

After starting the application, you can access the API at `http://localhost:8000`.

### Docker
To run the code within Docker, run `docker-compose up` in the root directory of the project.
Add the -d flag to run the containers in the background: `docker-compose up -d`.

### Local / Development
To run the code without Docker, run the following command:
```bash
python ./src/app.py
```