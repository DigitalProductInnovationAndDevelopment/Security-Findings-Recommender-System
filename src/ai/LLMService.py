from __future__ import annotations

import os
import requests
import json

from typing import List

from src.data.Finding import Finding, FindingKind

DEFAULT_PATH = "http://localhost:11434"
DEFAULT_MODEL = "llama3:instruct"


def answer_in_json_promt(key: str) -> str:
    return 'Answer in the following JSON format: {"' + key + '":"<your_selection>"}\n\n'


def clean(text: str | List[str], split_paragraphs=False) -> str | List[str]:
    if isinstance(text, list):
        # strip and if in the first 5 chars there is a ':', remove everything before it
        flattened = [item for sublist
                     in [clean(t).split("\n\n")
                         if split_paragraphs
                         else clean(t) for t in text]
                     for item in sublist]
        return flattened
    if isinstance(text, float):
        print(f"Float found: {text}")  # Why would there be a float? Noone knows. But it happened, so we are prepared.
        return str(text)
    if isinstance(text, dict):  # Also happened. LLMs are unpredictable.
        print(f"Dict found: {text}")
        return str(text)  # TODO: Here, we could use the llm to convert it more smartly.
    return text.strip()


class LLMService:
    """
    A class to interact with the OLLAMA API.
    """

    def __init__(self, model_url=None, model_name=None):
        if model_url is None:
            model_url = os.getenv("OLLAMA_URL", DEFAULT_PATH)
        if model_name is None:
            model_name = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)

        self.pull_url = model_url + "/api/pull"
        self.generate_url = model_url + "/api/generate"
        self.model_name = model_name

        self.generate_payload = {
            "model": self.model_name,
            "stream": False,
            "format": "json",
        }

        self.init_pull_model()

    def init_pull_model(self):
        """
        ATTENTION: If the model is not cached, this function will take a long time to execute.
        Pulls the model from the OLLAMA API.

        :return: None
        """
        payload = {
            "name": self.model_name
        }
        response = requests.post(self.pull_url, json=payload)
        response.raise_for_status()

    def get_model_name(self) -> str:
        return self.model_name

    def generate(self, prompt: str) -> dict:
        """
        Queries the model with the given prompt. Parses the response and returns it.
        :param prompt: The prompt to query the model with.
        :return: the parsed response from the model.
        """
        payload = {
            "prompt": prompt,
            **self.generate_payload
        }
        response = requests.post(self.generate_url, json=payload)
        response.raise_for_status()
        try:
            json_response = response.json()
            return json.loads(json_response['response'], strict=False)
        except json.JSONDecodeError as e:
            return {}

    def classify_kind(self, finding: Finding, options: FindingKind = None) -> FindingKind:
        """
        Queries the model with the given finding to classify its kind.
        :param finding: The finding to classify.
        :param options: The options to choose from.
        :return: the classified kind of the finding.
        """

        if options is None:
            options = list(FindingKind)

        options_str = ', '.join([kind.name for kind in options])
        prompt = f"Classify the following security finding. The options are: {options_str}\n" \
                 f"{answer_in_json_promt('selected_option')}" \
                 f"[DATA]\n{str(finding)}\n[/DATA]"
        response = self.generate(prompt)
        if 'selected_option' not in response:
            print(f"Failed to classify the finding: {finding.title}")
            return FindingKind.DEFAULT  # Default to DEFAULT if no option is selected
        return FindingKind[response['selected_option']]

    def get_recommendation(self, finding: Finding, short=True) -> str:
        """
        Queries the model with the given finding to generate a recommendation.
        :param short:
        :param finding: The finding to generate a recommendation for.
        :return: the generated recommendation.
        """
        prompt = f"Explain how to fix the following security finding. \n\n"

        if short:
            prompt += self._generate_short_recommendation_prompt()
        else:
            prompt += self._generate_long_recommendation_prompt(finding)

        prompt += f"[DATA]\n{str(finding)}\n[/DATA]"
        finding.solution.add_to_metadata(f"prompt_{'short' if short else 'detailed'}", prompt)

        response = self.generate(prompt)

        if 'recommendation' not in response:
            error_message = f"Failed to generate a {'short' if short else 'long'} recommendation for the finding: {finding.title}"
            print(error_message)
            return '[SYSTEM] Failed to generate recommendation.' if short else [
                '[SYSTEM] Failed to generate recommendation.']

        return clean(response['recommendation'])

    def _generate_short_recommendation_prompt(self) -> str:
        return f"Keep it short and concise, answer in maximum 2 sentences.\n\n{answer_in_json_promt('recommendation')}"

    def _generate_long_recommendation_prompt(self, finding: Finding, meta_prompting_enabled=True) -> str:
        if meta_prompting_enabled and (finding.solution and finding.solution.short_description):
            finding.solution.add_to_metadata("used_meta_prompt", True)
            return self._generate_prompt_with_meta_prompts(finding)
        else:
            return self._generate_generic_long_recommendation_prompt()

    def _generate_prompt_with_meta_prompts(self, finding: Finding) -> str:
        short_recommendation = finding.solution.short_description
        meta_prompt_generator = self._generate_meta_prompt_generator(finding.category.name, short_recommendation)
        meta_prompt_response = self.generate(meta_prompt_generator)
        meta_prompts = clean(meta_prompt_response.get('meta_prompts', ''))

        return (f"Based on the following short recommendation:\n"
                f"{short_recommendation}\n\n"
                f"Provide a comprehensive and self-contained step-by-step solution for the security finding. "
                f"Expand upon the key points mentioned in the short recommendation, adding more detail and specific instructions. "
                f"{meta_prompts}\n"
                f"Include the following in your response:\n"
                f"- Links to relevant documentation or resources, if necessary.\n"
                f"- Any potential caveats or considerations to keep in mind.\n\n"
                f"Answer in JSON format: {{\"recommendation\":[\"<Step_1_Text>\", \"<Step_2_Text>\", ...]}}.\n\n")

    def _generate_meta_prompt_generator(self, category: str, short_recommendation: str) -> str:
        return (f"Based on the following information:\n"
                f"Category: {category}\n"
                f"Short Recommendation: {short_recommendation}\n\n"
                f"Generate a prompt that guides the generation of a comprehensive step-by-step solution for the security finding. "
                f"The prompt should focus on eliciting actionable steps, relevant details, and specific instructions. "
                f"Consider the following aspects while generating the prompt:\n"
                f"- Request for version numbers or releases to upgrade to, if applicable\n"
                f"- Ask for exact commands, code snippets, or configuration changes required\n"
                f"- Encourage providing links to relevant documentation or resources\n"
                f"- Remind to include any potential caveats or considerations\n\n"
                f"Please provide the generated prompt in the following JSON format:\n"
                f"{answer_in_json_promt('meta_prompts')}")

    def _generate_generic_long_recommendation_prompt(self) -> str:
        return (f"Provide a comprehensive and self-contained step-by-step solution for the following security finding. "
                f"Be detailed and specific in each step, ensuring that the user has all the information needed to implement the solution without further research. "
                f"Include the following in your response:\n"
                f"- Specific version numbers or releases to upgrade to, if applicable.\n"
                f"- Exact commands, code snippets, or configuration changes required.\n"
                f"- Links to relevant documentation or resources, if necessary.\n"
                f"- Any potential caveats or considerations to keep in mind.\n\n"
                f"Answer in JSON format: {{\"recommendation\":[\"<Step_1_Text>\", \"<Step_2_Text>\", ...]}}.  ")

    def get_search_terms(self, finding: Finding) -> List[str]:
        """
        Queries the model with the given finding to generate search terms.
        :param finding: The finding to generate search terms for.
        :return: the generated search terms.
        """
        prompt = f"Generate search terms for future research into the following security finding.\n" \
                 f"Use ';' as seperator.\n\n" \
                 f"{answer_in_json_promt('search_terms')}" \
                 f"[DATA]\n{str(finding)}\n[/DATA]"
        response = self.generate(prompt)
        if 'search_terms' not in response:
            print(f"Failed to generate search terms for the finding: {finding.title}")
            return []
        return clean(response['search_terms'])
