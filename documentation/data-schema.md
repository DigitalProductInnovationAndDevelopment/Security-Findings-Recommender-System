# Data Schema

This document provides a detailed description of the data formats used by the Security Findings Recommender System.

![Architecture Diagram](UML/data-layer.svg)

## VulnerabilityReport Object

The `VulnerabilityReport` object represents the entire vulnerability report.

### Structure

```json
{
  "findings": [
    {
      "title": "List of titles",
      "source": "Set of sources",
      "description": "List of descriptions",
      "location_list": "List of locations",
      "cwe_ids": "List of CWE IDs",
      "cve_ids": "List of CVE IDs",
      "severity": "Severity level (integer)",
      "priority": "Priority level (integer)",
      "category": "Category (optional)",
      "solution": "Solution object (optional)"
    }
  ]
}
```

## Finding Object
The `Finding object` represents a single security finding.

### Structure

```json
{
  "title": "List of titles",
  "source": "Set of sources",
  "description": "List of descriptions",
  "cwe_ids": "List of CWE IDs",
  "cve_ids": "List of CVE IDs",
  "severity": "Severity level (integer)",
  "priority": "Priority level (integer)",
  "category": "Category (optional)",
  "solution": "Solution object (optional)"
}
```

### Fields
- title: A list of titles for the finding.
- source: A set of sources where the finding was identified.
- description: A list of descriptions providing details about the finding.
- cwe_ids: A list of Common Weakness Enumeration (CWE) IDs associated with the finding.
- cve_ids: A list of Common Vulnerabilities and Exposures (CVE) IDs associated with the finding.
- severity: An integer representing the severity level of the finding.
- priority: An integer representing the priority level of the finding.
- category: A string representing the category of the finding (optional).
- solution: A Solution object providing details for addressing the finding (optional).

## Solution Object
The Solution object represents a solution for a security finding.

### Structure

```json
{
  "short_description": "Short description of the solution",
  "long_description": "Detailed description of the solution",
  "search_terms": "List of search terms"
}
```

### Fields
- short_description: A brief description of the solution.
- long_description: A detailed description of the solution.
- search_terms: A list of search terms associated with the solution.

## AggregatedSolution Object
The AggregatedSolution object represents a solution that has been aggregated for multiple findings.

### Structure
```json
{
  "findings": [
    "List of Finding objects"
  ],
  "solution": "Aggregated solution description",
  "metadata": "Dictionary of additional metadata"
}
```

### Fields

- findings: A list of `Finding` objects that the solution addresses.
- solution: A description of the aggregated solution.
- metadata: A dictionary containing additional metadata about the aggregated solution.

## FindingKind Enum

The `FindingKind` enum represents the different categories of security findings.

### Categories

- **SYSTEM**: System-related findings.
- **USER**: User-related findings.
- **CODE**: Code-related findings.
- **DEFAULT**: Default category for uncategorized findings.

## Data Conversion Methods

- **VulnerabilityReport.to_dict()**  
  Returns a list of dictionaries, where each dictionary represents a `Finding` object.

- **Finding.to_dict()**  
  Returns a dictionary representing the `Finding` object.

- **Solution.to_dict()**  
  Returns a dictionary representing the `Solution` object.

- **AggregatedSolution.to_dict()**  
  Returns a dictionary representing the `AggregatedSolution` object.

# Example Data Structures

### VulnerabilityReport Example:

```json
{
  "findings": [
    {
      "title": ["Example Finding"],
      "source": ["Source 1", "Source 2"],
      "description": ["This is an example finding."],
      "location_list": ["Location 1", "Location 2"],
      "cwe_ids": ["CWE-79"],
      "cve_ids": ["CVE-2021-12345"],
      "severity": 5,
      "priority": 1,
      "category": "CODE",
      "solution": {
        "short_description": "Example Solution",
        "long_description": "This is a detailed description of the example solution.",
        "search_terms": ["example", "solution"]
      }
    }
  ]
}
```

### Finding Example:
```json
{
  "title": ["Example Finding"],
  "source": ["Source 1", "Source 2"],
  "description": ["This is an example finding."],
  "cwe_ids": ["CWE-79"],
  "cve_ids": ["CVE-2021-12345"],
  "severity": 5,
  "priority": 1,
  "category": "CODE",
  "solution": {
    "short_description": "Example Solution",
    "long_description": "This is a detailed description of the example solution.",
    "search_terms": ["example", "solution"]
  }
}
```

### Solution Example
```json
{
  "short_description": "Example Solution",
  "long_description": "This is a detailed description of the example solution.",
  "search_terms": ["example", "solution"]
}
```

### AggregatedSolution Example
```json
{
  "findings": [
    {
      "title": ["Example Finding 1"],
      "source": ["Source 1"],
      "description": ["This is an example finding 1."],
      "cwe_ids": ["CWE-79"],
      "cve_ids": ["CVE-2021-12345"],
      "severity": 5,
      "priority": 1,
      "category": "CODE",
      "solution": {
        "short_description": "Example Solution 1",
        "long_description": "This is a detailed description of the example solution 1.",
        "search_terms": ["example", "solution"]
      }
    },
    {
      "title": ["Example Finding 2"],
      "source": ["Source 2"],
      "description": ["This is an example finding 2."],
      "cwe_ids": ["CWE-89"],
      "cve_ids": ["CVE-2021-67890"],
      "severity": 3,
      "priority": 2,
      "category": "USER",
      "solution": {
        "short_description": "Example Solution 2",
        "long_description": "This is a detailed description of the example solution 2.",
        "search_terms": ["example", "solution"]
      }
    }
  ],
  "solution": "Aggregated solution for multiple findings.",
  "metadata": {
    "aggregation_method": "example method"
  }
}
```