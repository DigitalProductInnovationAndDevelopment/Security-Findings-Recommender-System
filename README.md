# Security-Findings-Recommender-System

## Introduction

to be written

## Pre-requisites

### Docker

To run the code within Docker, you should install Docker Desktop from [the official website](https://www.docker.com/products/docker-desktop).

### Local / Development

To run the code without Docker, follow these steps:

- Install Python 3.9 or higher from [the official website](https://www.python.org/downloads/).
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

### Environment

Copy the `.env.example` file to `.env` and fill in the required values.

## Usage

After starting the application, you can access the API at `http://localhost:8000`.

### Docker

To run the code within Docker, run `docker-compose up` in the root directory of the project.
Add the -d flag to run the containers in the background: `docker-compose up -d`.

### Database

Database models are constructed using SQLAlchemy and can be found in the `src/models` directory. You can make changes to the data types as needed.

To migrate your changes, use the following command in the Makefile, replacing `mention_changes_here_in_short` with a brief description of your changes:

```bash
make db-schema name="mention_changes_here_in_short"
```

After running the above command, you can migrate your changes to the database. Ensure that the database is up and running before you do this:

```
make db-migrate
```

### Local / Development

To run the code without Docker, run the following command:

```bash
cd src && python app.py
```

### NOTE

To run the app, always execute it from the `src` folder to avoid issues with import paths.
