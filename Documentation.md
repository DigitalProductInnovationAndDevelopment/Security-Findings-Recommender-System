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

## Data Types

The `VulnerabilityReport`, `Finding`, and `Solution` classes provide `to_dict` methods that convert the objects to dictionary representations. Here's an overview of the data types and structures returned by these methods:

### `VulnerabilityReport.to_dict()`

Returns a list of dictionaries, where each dictionary represents a `Finding` object:

```python
[
    {
        'title': List[str],
        'source': Set[str],
        'description': List[str],
        'cwe_ids': List[str],
        'cve_ids': List[str],
        'severity': int,
        'priority': int,
        'category': str (optional),
        'solution': dict (optional)
    },
    ...
]
```

### `Finding.to_dict()`

Returns a dictionary representing the `Finding` object:

```python
{
    'title': List[str],
    'source': Set[str],
    'description': List[str],
    'cwe_ids': List[str],
    'cve_ids': List[str],
    'severity': int,
    'priority': int,
    'category': str (optional),
    'solution': dict (optional)
}
```

The `category` field is included only if it is not `None` or `FindingKind.DEFAULT`. The `solution` field is included only if a solution has been generated for the finding.

### `Solution.to_dict()`

Returns a dictionary representing the `Solution` object:

```python
{
    'short_description': str,
    'long_description': str,
    'search_terms': str
}
```

The `search_terms` field is an empty list if no search terms have been generated for the solution.

These dictionary representations provide a structured way to access and manipulate the data contained in the `VulnerabilityReport`, `Finding`, and `Solution` objects. They can be useful for serialization, storage, or integration with other systems.

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