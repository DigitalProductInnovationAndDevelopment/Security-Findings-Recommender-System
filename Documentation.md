# Security Findings Recommender

This Python code generates vulnerability reports using AI-powered analysis and recommendations. It takes JSON data from a Flama export, creates a `VulnerabilityReport` object containing `Finding` objects, and enhances the findings with AI-generated categories and solutions.

## Key Components

1. `VulnerabilityReport` class:
   - Represents the entire vulnerability report.
   - Contains a list of `Finding` objects.
   - Provides methods to add categories and solutions to the findings.
   - Can be sorted by severity or priority.
   - Supports conversion to dictionary, string, and HTML representations.

2. `Finding` class:
   - Represents a single security finding.
   - Contains information such as title, source, description, CWE IDs, CVE IDs, severity, and priority.
   - Uses an `LLMService` to add AI-generated categories and solutions.
   - Supports conversion to dictionary, string, and HTML representations.

3. `Solution` class:
   - Represents a solution for a security finding.
   - Contains a short description, a long description, and search terms.
   - Supports conversion to dictionary, string, and HTML representations.

4. `LLMService` class:
   - Interacts with the OLLAMA API to generate AI-powered recommendations.
   - Provides methods to classify the kind of a finding, generate recommendations, and generate search terms.
   - Uses JSON prompts to format the input and output data.

5. `FindingKind` enum:
   - Represents the different categories of security findings (SYSTEM, USER, CODE, DEFAULT).

## Usage

1. Load the JSON data from a Flama export.
2. Create a `VulnerabilityReport` object using the `create_from_flama_json` function.
3. Add categories to the findings using the `add_category` method.
4. Add solutions to the findings using the `add_solution` method.
5. Sort the findings by severity or priority using the `sort` method.
6. Access the findings and their details using the `get_findings` method or convert the report to various formats using the `to_dict`, `__str__`, or `to_html` methods.

## Dependencies

- `tqdm`: Used for progress bars during category and solution generation.
- `requests`: Used for making HTTP requests to the OLLAMA API.
- `json`: Used for JSON parsing and formatting.

## Configuration

- The `LLMService` class uses environment variables for configuration:
  - `OLLAMA_URL`: The URL of the OLLAMA API (default: "http://localhost:11434").
  - `OLLAMA_MODEL`: The name of the OLLAMA model to use (default: "llama3:instruct").

## Example

An example usage of the code can be found in the `how_to_data_schema.ipynb` notebook. It demonstrates how to load JSON data, create a `VulnerabilityReport`, add categories and solutions to the findings, and display the results.