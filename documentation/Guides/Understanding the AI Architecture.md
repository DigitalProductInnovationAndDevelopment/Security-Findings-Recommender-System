# Understanding the AI Architecture: A Deep Dive

## Introduction

Our application's AI component is built on a flexible, extensible architecture designed to accommodate various Large Language Model (LLM) services. This design allows for easy integration of new LLM providers while maintaining a consistent interface for the rest of the application. The system currently supports [OpenAI's GPT models](https://platform.openai.com/docs/models), [Anthropic's models](https://docs.anthropic.com/en/docs/about-claude/models), and [Ollama's library of models](https://ollama.com/library), with the capability to easily integrate additional providers.

## Core Architectural Principles

### Abstraction and Polymorphism

The foundation of our design is the [`BaseLLMService`](all.py) abstract base class. This class defines a common interface for all LLM services, embodying the principle of abstraction. Key abstract methods include:

- `get_model_name()`
- `get_context_size()`
- `get_url()`
- `_generate(prompt: str, json=False)`
- `combine_descriptions(descriptions: List[str])`

By defining these methods, we create a contract that all concrete LLM service implementations must fulfill, enabling polymorphic behavior throughout the system.

### Strategy Pattern

The [`LLMServiceStrategy`](all.py) class implements the Strategy pattern, allowing the application to switch between different LLM services at runtime. This design choice provides flexibility and facilitates easy A/B testing or fallback mechanisms. It delegates calls to the current strategy (LLM service), handling tasks such as:

- Generating responses
- Classifying findings
- Getting recommendations
- Generating search terms
- Creating aggregated solutions

### Mixin for Shared Functionality

The [`LLMServiceMixin`](all.py) class employs the Mixin pattern to provide common utility methods across different LLM service implementations. This approach promotes code reuse and ensures consistent handling of tasks like:

- API key management
- Response cleaning
- JSON parsing
- Error handling

## Extensibility and Service Integration

To integrate a new LLM service, create a new class that inherits from `BaseLLMService` and `LLMServiceMixin`. This new class must implement the abstract methods defined in `BaseLLMService`, tailoring them to the specific API and requirements of the new LLM service.

The [`OpenAIService`](OpenAIService.py) and [`OLLAMAService`](OLLAMAService.py) classes serve as concrete examples of this integration pattern. Each implements the required methods while handling the unique aspects of their respective APIs.

Steps for adding a new LLM service:

1. Create a new class inheriting from `BaseLLMService` and `LLMServiceMixin`.
2. Implement all abstract methods from `BaseLLMService`.
3. Override `LLMServiceMixin` methods if necessary for service-specific behavior.
4. Create service-specific prompt templates.
5. Implement the `_generate` method to handle API interactions.
6. Add any necessary service-specific methods or attributes.

For more detailed instructions, refer to the [LLM Service Integration Guide](LLM%20Service%20Integration%20Guide.md).

## Prompt Engineering and Response Processing

Each service implementation contains methods for constructing prompts and processing responses. This separation allows for fine-tuning prompts and response handling for each specific LLM service.

Key methods include:

- `_get_classification_prompt(options: str, field_name: str, finding_str: str)`
- `_get_recommendation_prompt(finding: Finding, short: bool)`
- `_process_recommendation_response(response: Dict[str, str], finding: Finding, short: bool)`
- `_get_search_terms_prompt(finding: Finding)`
- `_process_search_terms_response(response: Dict[str, str], finding: Finding)`

For example, in the `OpenAIService`, the `_get_classification_prompt` method uses a template to generate a prompt for classifying findings:

```python
def _get_classification_prompt(self, options: str, field_name: str, finding_str: str) -> str:
    return OPENAI_CLASSIFY_KIND_TEMPLATE.format(options=options, field_name=field_name, data=finding_str)
```

## Handling Complex Tasks: FindingGrouper and FindingBatcher

The [`FindingGrouper`](grouping.py) class demonstrates how our architecture handles more complex AI tasks. It works in conjunction with the [`FindingBatcher`](grouping.py) to process and group findings efficiently.

### FindingBatcher

The `FindingBatcher` is responsible for creating batches of findings that fit within the LLM's context size. It uses methods like:

- `create_batches(findings: List[Finding])`
- `_fits_in_context(findings: List[Finding], include_solution: bool)`
- `_recursive_batch(findings: List[Finding], depth: int = 0)`

### FindingGrouper

The `FindingGrouper` uses the `FindingBatcher` to create appropriately sized batches of findings, then leverages the chosen LLM service to generate aggregated solutions. Key methods include:

- `generate_aggregated_solutions()`
- `_get_subdivision_prompt(findings: List[Finding])`
- `_process_subdivision_response(response: Dict, findings: List[Finding])`

This approach showcases how higher-level components can build upon the base LLM service interface to perform sophisticated operations while remaining agnostic to the specific LLM service being used.

## Examples of Correct Usage

Here are some examples of how to use the LLM services:

1. Classifying a finding:

```python
result = llm_service.classify_kind(finding, "severity_level", SeverityLevel)
```

2. Getting a recommendation:

```python
short_recommendation = llm_service.get_recommendation(finding, short=True)
long_recommendation = llm_service.get_recommendation(finding, short=False)
```

3. Generating search terms:

```python
search_terms = llm_service.get_search_terms(finding)
```

4. Generating an aggregated solution:

```python
aggregated_solutions = llm_service.generate_aggregated_solution(findings)
```

## Conclusion

Our AI architecture exemplifies key software design principles: abstraction, polymorphism, and separation of concerns. By providing a flexible foundation, it allows for easy integration of new LLM services and adaptation to evolving AI technologies, all while maintaining a consistent interface for the rest of the application.

This design not only accommodates current needs but also positions the system for future enhancements and adaptations in the rapidly evolving field of AI and large language models. Understanding these architectural principles and patterns is crucial for effectively working with and extending the AI capabilities of our application.