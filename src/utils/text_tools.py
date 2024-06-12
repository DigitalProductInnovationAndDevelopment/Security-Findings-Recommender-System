from typing import Union, List


def get_list_from_str_with_word(text: str, seperator: str) -> List[str]:
    """
    splits before seperator without removing it
    :param text:  The text to split.
    :param seperator:  The seperator to split on.
    :return:  A list of strings.
    """
    return [seperator + x for x in text.split(seperator)][:-1]


def clean(text: Union[str, List[str]], llm_service=None) -> str:
    if isinstance(text, list):
        clean_items = [clean(item, llm_service) for item in text]
        return "\n".join(clean_items)
    if isinstance(text, dict):  # Also happened. LLMs are unpredictable.
        return convert_dict_to_str(text, llm_service=llm_service)
    return str(text).strip()


def convert_dict_to_str(data: dict, llm_service=None) -> str:
    if llm_service is None:
        from src.ai.LLM.LLMServiceStrategy import LLMServiceStrategy  # Lazy import to avoid circular imports
        llm_service = LLMServiceStrategy()
    return llm_service.convert_dict_to_str(data)
