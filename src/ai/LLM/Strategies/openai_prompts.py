CLASSIFY_KIND_TEMPLATE = (
    "You are a cybersecurity and IT expert. Classify the following security finding in the category {field_name}. The options are: {options}, NotListed\n"
    "Choose NotListed if none of the options fit." +
    f"Just answer with your selected Option, nothing else." +
    "[DATA]\n{data}\n[/DATA]"
)

SHORT_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Explain how to fix the following security finding.\n\n"
    "Keep it short and concise, answer in maximum 2 sentences.\n\n"
    "[DATA]\n{data}\n[/DATA]"
)

LONG_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert.\n"
    "{meta_prompts}\n\n"
    "Write at least two paragraphs, each representing one step to the solution. Maximum is ten paragraphs.\n"
)

META_PROMPT_GENERATOR_TEMPLATE = (
    "You are an AI prompt engineering expert. Based on the following information:\n\n"
    "\n {finding}\n\n"
    "Generate a prompt that guides the generation of a comprehensive step-by-step solution for the security finding. "
    "The prompt should focus on eliciting actionable steps, relevant details, and specific instructions. "
    "The prompt does not include anything about output format."
    "Consider the following aspects while generating the prompt:\n"
    "- Request for version numbers or releases to upgrade to, if applicable\n"
    "- Ask for exact commands, code snippets, or configuration changes required\n"
    "- Encourage providing links to relevant documentation or resources\n"
    "- Stress that the response should be self-contained and detailed\n"
    "- Remind to include any potential caveats or considerations\n"
    "- Stress that the response should be human-readable text and may include MarkDown, if applicable\n\n"
    "Do not repeat this prompt in your response. Do not introduce the prompt."
)

GENERIC_LONG_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Provide a comprehensive and self-contained step-by-step solution for the following security finding. "
    "Be detailed and specific in each step, ensuring that the user has all the information needed to implement the solution without further research. "
    "Include the following in your response:\n"
    "- Specific version numbers or releases to upgrade to, if applicable.\n"
    "- Exact commands, code snippets, or configuration changes required.\n"
    "- Links to relevant documentation or resources, if necessary.\n"
    "- Any potential caveats or considerations to keep in mind.\n\n"
    "The text can be extensive and include MarkDown if appropriate.\n"
)

SEARCH_TERMS_TEMPLATE = (
    "You are an information retrieval expert.\n"
    "Generate five to ten search terms for future research into the following security finding.\n "
    "Just return the search terms as a list of strings.\n"
    "Use ';' as separator.\n\n"
    "[DATA]\n{data}\n[/DATA]"
)

CONVERT_DICT_TO_STR_TEMPLATE = (
    "You are a data formatting expert. Convert the following dictionary into a human-readable string. "
    "[DATA]\n{data}\n[/DATA]"
)