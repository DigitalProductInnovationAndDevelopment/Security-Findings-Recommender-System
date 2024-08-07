# Introduction

## Security Findings Recommender System

### Overview

The Security Findings Recommender System is a sophisticated tool designed to assist users in identifying and managing security vulnerabilities. Leveraging AI-powered analysis, the system generates detailed reports that categorize findings and provide actionable recommendations. This tool processes JSON data from a Flama export, creating a comprehensive `VulnerabilityReport` that includes individual `Finding` objects, each enriched with AI-generated categories and solutions.

### Project Goals

- **Automate Vulnerability Reporting:** Streamline the process of generating vulnerability reports from raw data.
- **Enhance Findings with AI:** Use AI to categorize findings and suggest solutions, making reports more informative and actionable.
- **Improve Security Management:** Help users prioritize and address security vulnerabilities effectively based on their severity and priority.

### High-level Architecture

The architecture of the Security Findings Recommender System is designed to be modular and scalable. The system consists of several key components that work together to process data, generate findings, and enhance these findings with AI-generated insights.

![Architecture Diagram](UML/data-layer.svg)

### Key Components

#### 1. VulnerabilityReport Class

- **Purpose:** Represents the entire vulnerability report.
- **Features:**
  - Contains a list of `Finding` objects.
  - Provides methods to add categories and solutions to the findings.
  - Can be sorted by severity or priority.
  - Supports conversion to dictionary, string, and HTML representations.

#### 2. Finding Class

- **Purpose:** Represents a single security finding.
- **Features:**
  - Includes details like title, source, description, CWE IDs, CVE IDs, severity, and priority.
  - Uses an `LLMService` to add AI-generated categories and solutions.
  - Supports conversion to dictionary, string, and HTML representations.

#### 3. Solution Class

- **Purpose:** Represents a solution for a security finding.
- **Features:**
  - Includes a short description, a long description, and search terms.
  - Supports conversion to dictionary, string, and HTML representations.

#### 4. LLMService Class

- **Purpose:** Interacts with the OLLAMA API to generate AI-powered recommendations.
- **Features:**
  - Provides methods to classify the type of finding, generate recommendations, and generate search terms.
  - Uses JSON prompts to format the input and output data.

### Benefits of Using This System

- **Efficiency:** Automates the time-consuming task of categorizing and prioritizing security findings.
- **Accuracy:** Leverages AI to provide accurate and relevant recommendations.
- **Usability:** Offers a user-friendly interface to view and manage security findings.

### Getting Started

To start using the Security Findings Recommender System, follow the installation and usage instructions provided in the [README](../README.md) file. Detailed setup and configuration instructions are available in the [Prerequisites](01-prerequisites.md) and [Installation](02-installation.md) documents.


### Additional Resources

- **[Prerequisites](01-prerequisites.md):** Environment setup and dependencies.
- **[Installation](02-installation.md):** Step-by-step installation guide.
- **[Usage](03-usage.md):** Instructions on how to use the system.

- **[Testing](04-testing.md):** Provides an explanation of the testing strategy and rules.

---

This document provides an overview of the Security Findings Recommender System, its goals, and its key components. For detailed instructions on setting up and using the system, please refer to the relevant sections in the documentation.
