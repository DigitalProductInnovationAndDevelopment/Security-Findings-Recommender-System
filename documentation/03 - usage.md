# Usage

## Accessing the Application

- **API:** Available at [http://localhost:8000](http://localhost:8000)
- **Dashboard:** Available at [http://localhost:3000](http://localhost:3000)

## Available Routes
For a complete list of available routes, refer to the [Swagger UI](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc) documentation.

- **HEAD, GET /openapi.json**: Access the OpenAPI specification.
- **HEAD, GET /docs**: Access the Swagger UI documentation.
- **HEAD, GET /docs/oauth2-redirect**: OAuth2 redirect URI.
- **HEAD, GET /redoc**: Access the ReDoc documentation.
- **GET /api/v1/tasks/**: Retrieve all tasks.
- **DELETE /api/v1/tasks/{task_id}**: Delete a specific task by ID.
- **DELETE /api/v1/tasks/**: Delete all tasks.
- **GET /api/v1/tasks/{task_id}/status**: Get the status of a specific task by ID.
- **POST /api/v1/recommendations/**: Create a new recommendation.
- **POST /api/v1/recommendations/aggregated**: Create aggregated recommendations.
- **POST /api/v1/upload/**: Upload data.
- **GET /**: Root endpoint.

## Example Requests

### GET /api/v1/tasks/

**Request:**
```bash
curl http://localhost:8000/api/v1/tasks/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "status": "completed"
  }
]
```

### POST /api/v1/recommendations/

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/recommendations/ -d '{"data": "sample"}' -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": 1,
  "recommendation": "Sample Recommendation"
}
```

## Common Use Cases

- **Generating Recommendations:** Post data to `/api/v1/recommendations/` to generate recommendations based on provided data.
- **Checking Task Status:** Get the status of tasks to monitor progress and outcomes.

Refer to the [Examples](examples.md) for more usage scenarios.

