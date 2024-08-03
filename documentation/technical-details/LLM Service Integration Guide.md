# LLM Service Integration Guide
**Design Insights and Extension Strategies**

## Table of Contents

1. [Introduction](#introduction)
2. [Core Design Philosophy](#core-design-philosophy)
3. [Design Patterns and Their Application](#design-patterns-and-their-application)
    - [Strategy Pattern: Interchangeable LLM Services](#strategy-pattern-interchangeable-llm-services)
    - [Mixin Pattern: Sharing Utility Functions](#mixin-pattern-sharing-utility-functions)
    - [Template Method Pattern: Customizing Service Behavior](#template-method-pattern-customizing-service-behavior)
4. [Extending the System: Adding a New LLM Service](#extending-the-system-adding-a-new-llm-service)
5. [Conclusion](#conclusion)

## Introduction

This document outlines the architecture and implementation strategies for **integrating new Large Language Model (LLM) services into our system**. Our framework is designed to accommodate multiple LLM providers, allowing for flexibility and scalability as the AI landscape evolves.

Key components of our system include:

1. `BaseLLMService`: An abstract base class that defines the interface for all LLM services.
2. `LLMServiceMixin`: A mixin class providing utility methods common across different LLM implementations.
3. `LLMServiceStrategy`: A class implementing the strategy pattern to manage and switch between different LLM services.

For detailed architectural information, refer to the [Architecture Documentation](../architecture.md).

The system currently supports [OpenAI's GPT models](https://platform.openai.com/docs/models), [Antrophics models](https://docs.anthropic.com/en/docs/about-claude/models) and [Ollama's library of models](https://ollama.com/library), with the capability to easily integrate additional providers.

This guide serves two primary purposes:
1. It aims to deepen your understanding of the system's architecture, design patterns, and the rationale behind key decisions. By providing these insights, we enable you to grasp the system's flexibility and power. 
2. Building on this foundation, the guide offers practical steps and considerations for integrating new LLM services. This dual approach ensures that you not only know how to extend the system but also comprehend why it's structured the way it is, empowering you (🚀) to make informed decisions when adding new services.

## Core Design Philosophy

Our system is built on the principle of extensibility without modification. This means we can add new LLM services without changing existing code.

### Key Insights:

1. **Abstraction of LLM Interactions**: `BaseLLMService` defines a common interface for all LLM services, allowing the rest of the system to interact with any LLM service in a uniform way.

2. **Separation of Concerns**: Each LLM service encapsulates its own logic for API interactions, prompt handling, and response processing.

3. **Flexibility in Implementation**: While we provide a common structure, each LLM service has the freedom to implement methods in ways that best suit its unique characteristics.

## Design Patterns and Their Application

### Strategy Pattern: Interchangeable LLM Services

The strategy pattern is the cornerstone of our design, allowing seamless switching between different LLM services.

#### Why it matters:
- Enables A/B testing of different LLM services
- Allows easy upgrades to newer models or services
- Facilitates fallback mechanisms if one service is unavailable

#### How it's implemented:
- `BaseLLMService` defines the strategy interface
- Concrete implementations (e.g., `OpenAIService`, `OLLAMAService`) provide specific behaviors
- `LLMServiceStrategy` acts as the context, delegating calls to the current strategy

### Mixin Pattern: Sharing Utility Functions

The `LLMServiceMixin` provides common utilities across different LLM services.

#### Why it matters:
- Reduces code duplication
- Ensures consistent handling of common tasks (e.g., API key management, error handling)
- Allows for easy updates to shared functionality

#### How to leverage it:
When adding a new LLM service, inherit from both `BaseLLMService` and `LLMServiceMixin`. Override mixin methods only when necessary for service-specific behavior.

### Template Method Pattern: Customizing Service Behavior

The `BaseLLMService` uses the template method pattern to define the skeleton of operations while allowing subclasses to override specific steps.

#### Why it matters:
- Provides a consistent structure across all LLM services
- Allows for customization of specific steps (e.g., prompt generation, response processing) without altering the overall algorithm

#### Key template methods:
- `_generate`: Core method for interacting with the LLM API
- `_get_classification_prompt`, `_get_recommendation_prompt`: Customize prompt generation
- `_process_recommendation_response`: Customize response processing

## Extending the System: Adding a New LLM Service

When adding a new LLM service, consider the following:

1. **API Interaction**: How does the new service expect requests? How does it return responses?
2. **Prompt Engineering**: Does the service require specific prompt formats for optimal performance?
3. **Response Processing**: Are there any unique aspects to the service's responses that need special handling?
4. **Error Handling**: What types of errors might be specific to this service?

### Steps for Integration:

1. Create a new class inheriting from `BaseLLMService` and `LLMServiceMixin`.
2. Implement the abstract methods from `BaseLLMService`.
3. Override `LLMServiceMixin` methods if necessary for service-specific behavior.
4. Create service-specific prompt templates.
5. Implement the `_generate` method to handle API interactions.
6. Add any necessary service-specific methods or attributes.

### Example: Key Considerations

```python
class NewLLMService(BaseLLMService, LLMServiceMixin):
    def __init__(self, config: Dict[str, Any]):
        LLMServiceMixin.__init__(self, config)
        # Consider: What configuration does this service need?
        # API keys, model identifiers, endpoint URLs?

    def _generate(self, prompt: str, json: bool = False) -> Dict[str, str]:
        # Consider: 
        # - How to structure the API request?
        # - How to handle rate limiting or quotas?
        # - What errors might occur and how to handle them?
        pass

    def _get_classification_prompt(self, options: str, field_name: str, finding_str: str) -> str:
        # Consider: 
        # - Does this service perform better with a specific prompt structure?
        # - Are there any service-specific tokens or formatting needed?
        return CLASSIFY_KIND_TEMPLATE.format(options=options, field_name=field_name, data=finding_str)

    def _process_recommendation_response(self, response: Dict[str, str], finding: Finding, short: bool) -> Union[str, List[str]]:
        # Consider:
        # - Does the service return responses in a unique format?
        # - Is any post-processing needed to standardize the output?
        pass
```

## Conclusion

By understanding the code and its design principles and patterns, you can effectively integrate new LLM services while maintaining consistency and leveraging existing infrastructure. Remember, the goal is to encapsulate service-specific logic within your new class while adhering to the common interface defined by `BaseLLMService`.

As you implement new services, consider contributing insights back to this guide. What challenges did you face? Are there new patterns or considerations that emerged? Your experiences can help future developers extend the system even further.