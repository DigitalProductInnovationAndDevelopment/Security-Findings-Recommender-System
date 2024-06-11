import logging
from typing import Union, List


def get_list_from_str_with_word(text: str, seperator: str) -> List[str]:
    """
    splits before seperator without removing it
    :param text:  The text to split.
    :param seperator:  The seperator to split on.
    :return:  A list of strings.
    """
    return [seperator + x for x in text.split(seperator)][:-1]


def clean(text: Union[str, List[str]], split_paragraphs=False, llm_service=None) -> Union[str, List[str]]:
    if isinstance(text, list):
        # strip and if in the first 5 chars there is a ':', remove everything before it
        flattened = [item for sublist
                     # find Step 1, Step 2, etc. and split before
                     in [get_list_from_str_with_word(clean(t), 'Step')
                         if split_paragraphs
                         else [clean(t)] for t in text]
                     for item in sublist]
        return flattened
    if isinstance(text, dict):  # Also happened. LLMs are unpredictable.
        return convert_dict_to_str(text, llm_service=llm_service)
    return str(text).strip()


def convert_dict_to_str(data: dict, llm_service=None) -> str:
    if llm_service is None:
        from src.ai.LLMService import LLMService  # Lazy import to avoid circular imports
        llm_service = LLMService()
    return llm_service.convert_dict_to_str(data)
