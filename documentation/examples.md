# Examples

## Example 1: Generating a Vulnerability Report

1. **Prepare Input Data:**
   - Ensure your input data is in the correct JSON format as specified in the [Data Schema](data-schema.md).

2. **Submit Data for Processing:**
   ```bash
   curl -X POST /api/v1/recommendations/ -d '{"input": "example data"}' -H "Content-Type: application/json"
   ```

3. **View Report:** 
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

## Example 3: Uploading Data

1. **Prepare Data for Upload:**
    - Ensure your data is in the correct format for upload.

2. **Upload Data:**
    ```bash
    curl -X POST /api/v1/upload/ -F 'file=@/path/to/your/file.json'
    ```

3. **Verify Upload:**

    - Check the response to ensure the data was uploaded successfully.

## Example 4: Creating Aggregated Recommendations

1. **Submit Data for Aggregated Recommendations:**

    ```bash
    curl -X POST /api/v1/recommendations/aggregated -d '{"input": "example aggregated data"}' -H "Content-Type: application/json"
    ```


2. **View Aggregated Recommendations:**

    - Access the aggregated recommendations via the API or Dashboard.


For more detailed usage scenarios and troubleshooting, please refer to the [Usage](usage.md) guide.