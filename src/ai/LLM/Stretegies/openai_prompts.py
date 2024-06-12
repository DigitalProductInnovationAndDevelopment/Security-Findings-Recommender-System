CLASSIFY_KIND_TEMPLATE = (
    "You are a cybersecurity and IT expert. Classify the following security finding. The options are: {options}\n" +
    f"Just answer with your selected Option, nothing else." +
    "[DATA]\n{data}\n[/DATA]"
)

SHORT_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Explain how to fix the following security finding.\n\n"
    "Keep it short and concise, answer in maximum 2 sentences.\n\n"
    "[DATA]\n{data}\n[/DATA]"
)

LONG_RECOMMENDATION_TEMPLATE = (
    "You are a cybersecurity and IT expert. Based on the following short recommendation:\n"
    "{short_recommendation}\n\n"
    "Provide a comprehensive and self-contained step-by-step solution for the security finding. "
    "Expand upon the key points mentioned in the short recommendation, adding more detail and specific instructions.\n\n"
    "{meta_prompts}\n\n"
    "Include the following in your response:\n"
    "- Links to relevant documentation or resources, if necessary.\n"
    "- Any potential caveats or considerations to keep in mind.\n\n"
    "The text can be extensive and include MarkDown if appropriate. "
    "Anwer with human-readable text. "
    "Write at least two paragraphs, each representing one step to the solution. Maximum is ten paragraphs.\n"
    "Short Recommendation: {short_recommendation}"
)

META_PROMPT_GENERATOR_TEMPLATE = (
    "You are an AI prompt engineering expert. Based on the following information:\n"
    "Category: {category}\n"
    "Short Recommendation: {short_recommendation}\n\n"
    "Generate a prompt that guides the generation of a comprehensive step-by-step solution for the security finding. "
    "The prompt should focus on eliciting actionable steps, relevant details, and specific instructions. "
    "The prompt does not include anything about output format."
    "Consider the following aspects while generating the prompt:\n"
    "- Request for version numbers or releases to upgrade to, if applicable\n"
    "- Ask for exact commands, code snippets, or configuration changes required\n"
    "- Encourage providing links to relevant documentation or resources\n"
    "- Remind to include any potential caveats or considerations\n"
    "Do not repeat this prompt in your response."
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
    "You are an information retrieval expert. Generate five to ten search terms for future research into the following security finding.\n"
    "Use ';' as separator.\n\n"
    "[DATA]\n{data}\n[/DATA]"
)

CONVERT_DICT_TO_STR_TEMPLATE = (
    "You are a data formatting expert. Convert the following dictionary into a human-readable string. "
    "[DATA]\n{data}\n[/DATA]"
)