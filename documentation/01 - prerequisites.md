# Prerequisites

## Environment Setup

### .env File

The project uses environment variables to manage configuration settings. Ensure you have a `.env` file in your project directory. You can create this file by copying **and adapting** the provided `.env.docker.example` file:

```bash
cp .env.docker.example .env.docker
```

# Project Setup Guide

After copying and adapting the file, open it and add your desired values for configuration.

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

### Ollama

The project relies on the Ollama API for generating AI-powered recommendations. Follow these steps to set up Ollama when running without Docker:

1. **Install Ollama:**

   - Download and install Ollama from the [official website](https://www.ollama.com/).

2. **Configure Ollama URL:**
   - Ensure the correct URL for the Ollama API is set in your `.env` file:
     ```env
     OLLAMA_URL=http://localhost:11434
     ```
3. **Download Ollama Models:**
   - Download the required Ollama models by running the following command:
     ```bash
     ollama pull <model-name>
     ```
   - Replace `<model-name>` with the name of the model you want to download. You can find available models on [OLLAMA's Library page](https://ollama.com/library).

## Summary | TLDR

Depending on your preference, you can choose to run the project using Docker or locally.

### Docker

- **Prerequisites:** Docker installed on your system.
- **Setup:** Copy and adapt the `.env.docker.example` file.
- **Installation:** Follow the [Docker Installation](02%20-%20installation#docker-installation) guide for further setup.

### Local Development

- **Prerequisites:** Python and Pipenv installed on your system.
- **Environment Setup:** Copy and adapt the `.env.docker.example` file.
- **Installation:** Follow the [Local Development Installation](02%20-%20installation#local-development-installation) guide for further setup.
