# Security Findings Recommender System

## Introduction

This project aims to create a recommender system for security findings. The system will help users discover relevant security findings based on their preferences and the findings' characteristics.

## Prerequisites

### Environment

Copy the `.env.docker.example` file to `.env.docker` and fill in the required values.

### Docker

To run the code within Docker, install Docker Desktop from [the official website](https://www.docker.com/products/docker-desktop).

### Local Development

To run the code without Docker, follow these steps:

1. Install Python 3.9 or higher from [the official website](https://www.python.org/downloads/).
2. (Optional) Create a virtual environment to isolate the dependencies:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

#### Ollama
When running outside of Docker, you need to install Ollama from [the official website](https://ollama.com/).
Make sure to set the correct url for the Ollama API in the `.env` file (usually `http://localhost:11434`).

## Usage

After starting the application, you can access the API at `http://localhost:8000`.

### Docker

To run the code within Docker, use the following command in the root directory of the project:

```bash
docker compose up
```

Add the `-d` flag to run the containers in the background: `docker compose up -d`.

#### Database

Database models are constructed using SQLAlchemy and can be found in the `src/models` directory. You can make changes to the data types as needed.

To migrate your changes, use the following command in the Makefile, replacing `mention_changes_here_in_short` with a brief description of your changes:

```bash
make db-schema name="mention_changes_here_in_short"
```

After running the above command, migrate your changes to the database. Ensure that the database is up and running before you do this:

```bash
make db-migrate
```

### Local Development

#### Preparations

If you plan to run this without Docker, e.g., because you want to run the Jupyter notebooks, copy the `.env.docker.example` file to `src/.env` and fill in the required values.

Make sure to set the `src` folder as the working directory for Python to ensure the imports work correctly.

#### Running the App

```bash
cd src && python app.py
```

#### Running the Jupyter Notebooks

We provide a set of Jupyter notebooks to help you get started with data analysis and model training. To run the notebooks, execute the following command:

```bash
cd src && pip install jupyterlab && python -m jupyterlab
```

Then, you can find the notebooks in the `notebooks` directory.

### Note

To run the app, always execute it from the `src` folder to avoid issues with import paths.