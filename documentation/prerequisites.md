# Prerequisites

## Environment Setup

### .env File

The project uses environment variables to manage configuration settings. Ensure you have a `.env` file in your project directory. You can create this file by copying the provided `.env.docker.example` file:

```bash
cp .env.docker.example .env.docker
```

# Project Setup Guide

After copying the file, open it and fill in the required values.

## Docker

To run the project within Docker, you need to have Docker installed on your system. Follow the instructions below to set up Docker:

1. **Install Docker:**

    - Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
   
2. **Verify Docker Installation:**

    - Open a terminal and run the following command to verify Docker is installed correctly:

        ```bash
        docker --version
        ```

    - This should print the Docker version installed on your machine.

## Local Development

If you prefer to run the project without Docker, ensure you have Python and Pipenv installed on your system. Follow these steps for the setup:

1. **Install Python:**
    - Download and install Python 3.11 or higher from the [official website](https://www.python.org/downloads/).

2. **Install Pipenv:**
    - Pipenv is used for creating virtual environments and managing packages. Install Pipenv by running:
      ```bash
      pip install pipenv
      ```

3. **Install Project Dependencies:**
    - Navigate to your project directory and install the required packages using Pipenv:
      ```bash
      pipenv install
      ```
    - If you are using `pytest` and `mypy`, install the development dependencies:
      ```bash
      pipenv install --dev
      ```

4. **Activate Virtual Environment:**
    - Enter the virtual environment shell:
      ```bash
      pipenv shell
      ```
    - If you prefer not to enter the shell, you can run commands directly using:
      ```bash
      pipenv run <command>
      ```


## Ollama

The project relies on the Ollama API for generating AI-powered recommendations. Follow these steps to set up Ollama:

1. **Install Ollama:**
   - Download and install Ollama from the [official website](https://www.ollama.com/).

2. **Configure Ollama URL:**
   - Ensure the correct URL for the Ollama API is set in your `.env` file:
     ```env
     OLLAMA_URL=http://localhost:11434
     ```


## Summary

Ensure the following prerequisites are met before running the project:

- **Docker** installed (if running within Docker)
- **Python 3.11** or higher installed
- **Pipenv** installed
- Project dependencies installed via Pipenv
- **Ollama** installed and configured

With these prerequisites in place, you can proceed to the [Installation](installation.md) guide for detailed instructions on setting up and running the project.
