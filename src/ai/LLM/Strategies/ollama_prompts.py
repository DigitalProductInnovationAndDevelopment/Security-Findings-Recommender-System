def answer_in_json_prompt(key: str) -> str:
    return 'Answer in the following JSON format: {{"' + key + '":"<your_answer>"}}\n\n'


COMBINE_DESCRIPTIONS_TEMPLATE = (
    "You are an expert in combining information. Combine the following descriptions into a single, coherent description that includes all relevant information.\n\n"
    "Provide a single concise paragraph that summarizes all the important information from these descriptions.\n\n"
    f"{answer_in_json_prompt('combined_description')}"
    "[DATA]\n{data}\n[/DATA]"
)

CLASSIFY_KIND_TEMPLATE = (
        "You are a cybersecurity and IT expert. Classify the following security finding in the category {field_name}. The options are: {options}, NotListed\n"
        "Choose NotListed if none of the options fit." +
        f"{answer_in_json_prompt('selected_option')}" +
        "[DATA]\n{data}\n[/DATA]"
)

SHORT_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Explain how to fix the following security finding.\n\n"
    "Keep it short and concise, answer in maximum 2 sentences.\n\n"
    f"{answer_in_json_prompt('recommendation')}"
    "[DATA]\n{data}\n[/DATA]"
)

LONG_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert.\n"
    "{meta_prompts}\n\n"
    f"{answer_in_json_prompt('recommendation')}"
)

META_PROMPT_GENERATOR_TEMPLATE = (
    "You are an AI prompt engineering expert. Based on the following information:\n\n"
    "\n {finding}\n\n"
    "Generate a prompt that guides the generation of a comprehensive step-by-step solution for the security finding. "
    "The prompt should focus on eliciting actionable steps, relevant details, and specific instructions. "
    "Consider the following aspects while generating the prompt:\n"
    "- Request for version numbers or releases to upgrade to, if applicable\n"
    "- Ask for exact commands, code snippets, or configuration changes required\n"
    "- Encourage providing links to relevant documentation or resources\n"
    "- Stress that the response should be self-contained and detailed.\n"
    "- Give an appropriate length for the response, e.g. two to ten paragraphs. If applicable, give examples of the expected structure\n"
    "- Remind to include any potential caveats or considerations\n"
    "- Stress that the response should be human-readable text and may include MarkDown, if applicable\n"
    "Do not include anything about output format in you prompt. "
    "In your answer, follow this format:\n"
    f"{answer_in_json_prompt('meta_prompts')}"
)

GENERIC_LONG_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Provide a comprehensive and self-contained step-by-step solution for the following security finding. "
    "Be detailed and specific in each step, ensuring that the user has all the information needed to implement the solution without further research. "
    "Include the following in your response:\n"
    "- Specific version numbers or releases to upgrade to, if applicable.\n"
    "- Exact commands, code snippets, or configuration changes required.\n"
    "- Links to relevant documentation or resources, if necessary.\n"
    "- Any potential caveats or considerations to keep in mind.\n\n"
    "Your response can be extensive and include MarkDown if appropriate.\n"
    f"{answer_in_json_prompt('recommendation')}"
)

SEARCH_TERMS_TEMPLATE = (
    "You are an information retrieval expert. Generate five to ten search terms for future research into the following security finding.\n"
    "Use ';' as separator.\n\n"
    f"{answer_in_json_prompt('search_terms')}"
    "[DATA]\n{data}\n[/DATA]"
)

CONVERT_DICT_TO_STR_TEMPLATE = (
    "You are a data formatting expert. Convert the following dictionary into a human-readable string. "
    f"{answer_in_json_prompt('converted_text')}"
    "[DATA]\n{data}\n[/DATA]"
)
