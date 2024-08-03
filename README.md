# Security Findings Recommender System

## Overview

The Security Findings Recommender System is designed to assist in identifying, managing, and reporting security vulnerabilities. Leveraging AI-powered analysis, the system generates detailed reports that categorize findings and provide actionable recommendations.

## Project Goals

- **Automate Vulnerability Reporting**: Streamline the process of generating vulnerability reports from raw data.
- **Enhance Findings with AI**: Use AI to categorize findings and suggest solutions.
- **Improve Security Management**: Help users prioritize and address security vulnerabilities based on severity and priority.

## Features

- AI-powered categorization and solution generation
- Customizable categories and solutions
- Detailed single finding solutions and aggregated vulnerability multi-finding reports
- API interface for easy integration

For a detailed architectural overview and component descriptions, refer to the [Project Architecture Documentation](documentation/architecture.md).

## System Overview

The system consists of three main layers:

1. **Data Layer**: Manages core data structures such as `VulnerabilityReport`, `Finding`, and `Solution`.
2. **Aggregation Layer**: Handles the grouping and processing of findings using classes like `FindingBatcher`, `FindingGrouper`, and `AgglomerativeClusterer`.
3. **LLM (Language Model) Layer**: Provides natural language processing capabilities through services such as `OLLAMAService` and `OpenAIService`.

For more details, see the [System Overview](documentation/SystemOverview.md).

## Prerequisites

### Environment Setup

- Copy the `.env.docker.example` file to `.env.docker` and fill in the required values.
- For running without Docker, ensure the correct URL for the Ollama API is set in your `.env` file: `OLLAMA_URL=http://localhost:11434`.

For detailed setup instructions, refer to the [Prerequisites Documentation](documentation/01%20-%20prerequisites.md).

## Installation
1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

### Docker (details in [Docker Installation Guide](documentation/02%20-%20installation.md#docker-installation))

2. **Build and run the application using Docker:**
```
docker compose up -d --build
```

### Local Development (details in [Local Development Guide](documentation/02%20-%20installation.md#local-development-installation)) 

2. **Set Up Environment Variables**:
    Ensure `.env` file is configured as per prerequisites.

3. **Install Dependencies**:
    ```bash
    pipenv install
    ```

4. **Run the Application**:
    ```bash
    cd src && pipenv shell
    python app.py
    ```

## Usage

### Accessing the Application

- **API**: Available at `http://localhost:8000`
- **Dashboard**: Available at `http://localhost:3000`

### Available Routes (exempt)

- **GET /api/v1/tasks/**: Retrieve all tasks.
- **DELETE /api/v1/tasks/{task_id}**: Delete a specific task by ID.
- **POST /api/v1/recommendations/**: Create a new recommendation.
- **POST /api/v1/recommendations/aggregated**: Create aggregated recommendations.
- **POST /api/v1/upload/**: Upload data.
- **GET /**: Root endpoint.

For a complete list of available routes, refer to the [API Routes Documentation](documentation/03%20-%20usage.md#available-routes).

### Example Requests

#### Generate Recommendations
```bash
curl -X POST http://localhost:8000/api/v1/recommendations/ -d '{"data": "sample"}' -H "Content-Type: application/json"
```

#### Check Task Status
```bash
curl http://localhost:8000/api/v1/tasks/1/status
```

For more usage examples, refer to the [Examples Documentation](documentation/examples.md).

## Development

### Local Development

To run the code without Docker, follow these steps:

1. **Install Dependencies**:
    ```bash
    pipenv install
    ```

2. **Activate Virtual Environment**:
    ```bash
    pipenv shell
    ```

3. **Run the Application**:
    ```bash
    cd src && python app.py
    ```


## FAQs

For common questions and troubleshooting, refer to the [FAQs Documentation](documentation/FAQ.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Project Information
This Project was created in the context of TUMs practical course [Digital Product Innovation and Development](https://www.fortiss.org/karriere/digital-product-innovation-and-development) by fortiss in the summer semester 2024.
The task was suggested by Siemens, who also supervised the project.

## Contact
To contact fortiss or Siemens, please refer to their official websites.

### Team Members
- [Ishwor Giri](mailto:i.giri@tum.de)
- [Niklas Minth](mailto:niklas.minth@tum.de)
- [Ruben Kaiser](mailto:ruben.kaiser@tum.de)
- [Sema Sen](mailto:sema.sen@tum.de)