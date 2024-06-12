from typing import Union, List


def clean(text: Union[str, List[str]], split_paragraphs=False) -> Union[str, List[str]]:
    if isinstance(text, list):
        # strip and if in the first 5 chars there is a ':', remove everything before it
        flattened = [item for sublist
                     in [clean(t).split("\n\n")
                         if split_paragraphs
                         else [clean(t)] for t in text]
                     for item in sublist]
        return flattened
    if isinstance(text, float):
        print(f"Float found: {text}")  # Why would there be a float? Noone knows. But it happened, so we are prepared.
        return str(text)
    if isinstance(text, dict):  # Also happened. LLMs are unpredictable.
        return convert_dict_to_str(text)
    return text.strip()


def convert_dict_to_str(data: dict) -> str:
    from ai.LLMService import LLMService  # Lazy import to avoid circular imports
    llm_service = LLMService()
    return llm_service.convert_dict_to_str(data)
