# LLM Service Integration Guide

## Introduction

This guide provides practical steps and considerations for integrating new Large Language Model (LLM) services into our system. Our framework is designed to accommodate multiple LLM providers, allowing for flexibility and scalability as the AI landscape evolves.

For a comprehensive understanding of the underlying architecture, please refer to the [Understanding the AI Architecture](Understanding%20the%20AI%20Architecture.md) guide.

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

## Best Practices for Integration

1. **Consistent Interface**: Ensure that your new service adheres to the interface defined by `BaseLLMService`. This maintains consistency across the system and allows for easy swapping of services.

2. **Error Handling**: Implement robust error handling, especially for API-related issues. Use the error handling methods provided by `LLMServiceMixin` where appropriate.

3. **Configuration Management**: Use the configuration management approach provided by `LLMServiceMixin` for handling API keys and other service-specific settings.

4. **Prompt Engineering**: Carefully design your prompts to get the best performance from the new LLM service. Consider creating service-specific prompt templates if needed.

5. **Response Processing**: Implement thorough response processing to handle any quirks or unique formats of the new service's responses.

6. **Testing**: Create comprehensive tests for your new service, including edge cases and error scenarios.

## Integration Checklist

- [ ] Created new class inheriting from `BaseLLMService` and `LLMServiceMixin`
- [ ] Implemented all abstract methods from `BaseLLMService`
- [ ] Created service-specific prompt templates if needed
- [ ] Implemented `_generate` method for API interaction
- [ ] Added error handling for service-specific issues
- [ ] Implemented response processing methods
- [ ] Added configuration management for API keys and other settings
- [ ] Created tests for the new service
- [ ] Updated documentation to include the new service

## Conclusion

By following this guide, you should be able to integrate new LLM services into the system while maintaining consistency with the existing architecture. Remember to refer to the existing implementations (`OpenAIService` and `OLLAMAService`) as examples, and don't hesitate to extend or modify the base classes if needed to accommodate unique features of new services.