import json
from typing import Any, Dict
import logging
from utils.text_tools import clean

logger = logging.getLogger(__name__)


class LLMServiceMixin:
    """
    A mixin class providing common utility methods for LLM services.

    This mixin should be used in conjunction with BaseLLMService implementations
    to provide shared functionality across different LLM services.

    Attributes:
        config (Dict[str, Any]): Configuration dictionary for the LLM service.

    The config dictionary should include the following keys:
        - api_key (str): The API key for the LLM service.
        - model (str, optional): The name of the model to use. Defaults to 'default_model'.
        - Additional service-specific configuration keys as needed.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLMServiceMixin.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the LLM service.
        """
        self.config = config

    def get_api_key(self) -> str:
        """
        Retrieve the API key from the configuration.

        Returns:
            str: The API key.

        Raises:
            ValueError: If the API key is not provided in the configuration.
        """
        api_key = self.config.get('api_key')
        if not api_key:
            raise ValueError("API key not provided in configuration")
        return api_key

    def get_model(self) -> str:
        """
        Retrieve the model name from the configuration.

        Returns:
            str: The model name, or 'default_model' if not specified.
        """
        return self.config.get('model', 'default_model')

    def clean_response(self, response: str) -> str:
        """
        Clean the response using the utility function from text_tools.

        Args:
            response (str): The raw response string.

        Returns:
            str: The cleaned response string.
        """
        return clean(response, llm_service=self)

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse a JSON response string into a dictionary.

        Args:
            response (str): The JSON response string.

        Returns:
            Dict[str, Any]: The parsed JSON as a dictionary, or an empty dict if parsing fails.
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {}

    def format_prompt(self, template: str, **kwargs) -> str:
        """
        Format a prompt template with the given keyword arguments.

        Args:
            template (str): The prompt template string.
            **kwargs: Keyword arguments to fill in the template.

        Returns:
            str: The formatted prompt string.
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing key in prompt template: {e}")
            return template

    def handle_api_error(self, e: Exception) -> Dict[str, str]:
        """
        Handle and log API errors.

        Args:
            e (Exception): The exception that occurred during the API call.

        Returns:
            Dict[str, str]: A dictionary containing the error message.
        """
        logger.error(f"API error occurred: {str(e)}")
        return {"error": str(e)}

    def convert_dict_to_str(self, data: Dict[str, Any]) -> str:
        """
        Convert a dictionary to a descriptive string.

        This method uses the LLM to generate a human-readable description of the dictionary.

        Args:
            data (Dict[str, Any]): The dictionary to convert.

        Returns:
            str: A string description of the dictionary, or the stringified dictionary if conversion fails.
        """
        prompt = self.format_prompt(
            "Convert the following dictionary to a descriptive string: {data}",
            data=json.dumps(data)
        )
        response = self.generate(prompt)
        if "error" in response:
            logger.info(f"Failed to convert dictionary to string, returning it as str conversion.")
            return str(data)
        return self.clean_response(response.get("response", str(data)))

    def generate(self, prompt: str) -> Dict[str, str]:
        """
        Generate a response using the LLM.

        This method should be implemented by the class that uses this mixin.

        Args:
            prompt (str): The input prompt for the LLM.

        Returns:
            Dict[str, str]: The generated response.

        Raises:
            NotImplementedError: If the method is not implemented by the using class.
        """
        raise NotImplementedError("The generate method must be implemented by the class using this mixin.")
