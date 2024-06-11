from __future__ import annotations

import os
import requests
import json

from typing import List

from src.data.Finding import Finding, FindingKind


def answer_in_json_promt(key: str) -> str:
    return 'Answer in the following JSON format: {"' + key + '":"<your_selection>"}\n\n'


def clean(text: str | List[str]) -> str | List[str]:
    if isinstance(text, list):
        # strip and if in the first 5 chars there is a ':', remove everything before it
        return [clean(t) for t in text]
    if ':' in text[:8]:
        return text.strip().split(':', 1)[-1].strip()
    if text.startswith("Step_") and text[5] == "_":
        return text[7:].strip()
    return text.strip()


class LLMService:
    """
    A class to interact with the OLLAMA API.
    """

    def __init__(self, model_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
                 model_name=os.getenv("OLLAMA_MODEL", "llama3:instruct")):
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
            return json.loads(json_response['response'])
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
            prompt += f"Keep it short and concise, answer in maximum 2 sentences.\n\n"
            prompt += f"{answer_in_json_promt('recommendation')}"
        else:
            prompt += (f"Provide a detailed step by step solution approach for the following security finding. "
                       f"Be detailed in each step! Always tell me how.\n\n")
            prompt += ('Answer in JSON format: {"recommendation":["<Step_1>", "<Step_2>", ...]}. ')
            # 'Use as many steps as you need, but at least 1.\n\n')
        prompt += f"[DATA]\n{str(finding)}\n[/DATA]"
        response = self.generate(prompt)
        if 'recommendation' not in response:
            print(f"Failed to generate a recommendation for the finding: {finding.title}")
            return ''
        return clean(response['recommendation'])

    def get_search_terms(self, finding: Finding) -> List[str]:
        """
        Queries the model with the given finding to generate search terms.
        :param finding: The finding to generate search terms for.
        :return: the generated search terms.
        """
        prompt = f"Generate search terms for future research into the following security finding.\n\n" \
                 f"{answer_in_json_promt('search_terms')}" \
                 f"[DATA]\n{str(finding)}\n[/DATA]"
        response = self.generate(prompt)
        if 'search_terms' not in response:
            print(f"Failed to generate search terms for the finding: {finding.title}")
            return []
        return clean(response['search_terms'])
