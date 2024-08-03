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
- **POST /api/v1/recommendations/**: Retrive a new recommendation.
- **POST /api/v1/recommendations/aggregated**: Retrive aggregated recommendations.
- **POST /api/v1/upload/**: Upload data.
- **GET /**: Root endpoint.

# Examples

## Example 1: Generating a Vulnerability Report

1. **Prepare Input Data:**

   - Ensure your input data is in the correct JSON format as specified in the `ApiSchema.py`.

2. **Submit Data for Processing:**

   ```bash
   curl -X POST /api/v1/upload/ -d INPUT_DATA -H "Content-Type: application/json"

   ```

   INPUT_DATA must be of type

```
{
    "force_update":true,
    "preferences":{
        "long_description":false,
        "search_terms":false,
        "aggregated_solutions":false
    },
    "data": FLAMMA_OUTPUT
}
```

3. **Verify Upload:**

   - Check the response to ensure the data was uploaded successfully.

4. **View Report:**
   - Access the generated report via the Dashboard or API endpoints.

## Example 2: Checking Task Progress

1. **Check Task Status:**

   ```bash
   curl /api/v1/tasks/1/status
   ```

2. **Interpret Response:**
   ```json
   {
     "task_id": 1,
     "status": "completed",
     "details": "Task completed successfully."
   }
   ```

## Example 4: Creating Aggregated Recommendations

1. **Retrive Aggregated Recommendations:**

   ```bash
   curl -X POST /api/v1/recommendations/aggregated -d '{}' -H "Content-Type: application/json"
   ```

2. **View Aggregated Recommendations:**

   - Access the aggregated recommendations via the API or Dashboard.
