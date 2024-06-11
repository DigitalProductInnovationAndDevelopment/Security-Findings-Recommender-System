def answer_in_json_prompt(key: str) -> str:
    return 'Answer in the following JSON format: {{"' + key + '":"<your_selection>"}}\n\n'


CLASSIFY_KIND_TEMPLATE = (
    "Classify the following security finding. The options are: {options}\n" +
    f"{answer_in_json_prompt('selected_option')}" +
    "[DATA]\n{data}\n[/DATA]"
)

SHORT_RECOMMENDATION_TEMPLATE = (
    "Explain how to fix the following security finding.\n\n"
    "Keep it short and concise, answer in maximum 2 sentences.\n\n"
    f"{answer_in_json_prompt('recommendation')}"
    "[DATA]\n{data}\n[/DATA]"
)

LONG_RECOMMENDATION_TEMPLATE = (
    "Based on the following short recommendation:\n"
    "{short_recommendation}\n\n"
    "Provide a comprehensive and self-contained step-by-step solution for the security finding. "
    "Expand upon the key points mentioned in the short recommendation, adding more detail and specific instructions.\n"
    "{meta_prompts}\n"
    "Include the following in your response:\n"
    "- Links to relevant documentation or resources, if necessary.\n"
    "- Any potential caveats or considerations to keep in mind.\n\n"
    "Format your response as a JSON object with a single 'recommendation' field containing an array of strings. "
    "Each string in the array should represent a sensible step in the solution. "
    "The step text can be extensive and include MarkDown if appropriate."
    # "Iff a step-by-step solution is not possible or appropriate for this query, put your solution in the first and single array element.\n\n"
    "Example JSON format:\n"
    "{{\n"
    '  "recommendation": [\n'
    '    "STEP_1_TEXT",\n'
    '    "STEP_2_TEXT",\n'
    '    "STEP_3_TEXT",\n'
    "    ...\n"
    "  ]\n"
    "}}\n\n"
    "Short Recommendation: {short_recommendation}"
)
META_PROMPT_GENERATOR_TEMPLATE = (
    "Based on the following information:\n"
    "Category: {category}\n"
    "Short Recommendation: {short_recommendation}\n\n"
    "Generate a prompt that guides the generation of a comprehensive step-by-step solution for the security finding. "
    "The prompt should focus on eliciting actionable steps, relevant details, and specific instructions. "
    "Consider the following aspects while generating the prompt:\n"
    "- Request for version numbers or releases to upgrade to, if applicable\n"
    "- Ask for exact commands, code snippets, or configuration changes required\n"
    "- Encourage providing links to relevant documentation or resources\n"
    "- Remind to include any potential caveats or considerations\n"
    "- Emphasize the importance of providing steps as separate items in a list\n"
    "- Stress the need for a complete and valid JSON response\n\n"
    "Do not include anything about output format in you prompt."
    "In your answer, follow this format.:\n"
    f"{answer_in_json_prompt('meta_prompts')}"
)

GENERIC_LONG_RECOMMENDATION_TEMPLATE = (
    "Provide a comprehensive and self-contained step-by-step solution for the following security finding. "
    "Be detailed and specific in each step, ensuring that the user has all the information needed to implement the solution without further research. "
    "Include the following in your response:\n"
    "- Specific version numbers or releases to upgrade to, if applicable.\n"
    "- Exact commands, code snippets, or configuration changes required.\n"
    "- Links to relevant documentation or resources, if necessary.\n"
    "- Any potential caveats or considerations to keep in mind.\n\n"
    'Answer in JSON format, replace the placeholders: {{"recommendation":["STEP_1_TEXT", "STEP_2_TEXT", ...]}}. '
)

SEARCH_TERMS_TEMPLATE = (
    "Generate search terms for future research into the following security finding.\n"
    "Use ';' as separator.\n\n"
    f"{answer_in_json_prompt('search_terms')}"
    "[DATA]\n{data}\n[/DATA]"
)

CONVERT_DICT_TO_STR_TEMPLATE = (
    "Convert the following dictionary into a human-readable string. "
    f"{answer_in_json_prompt('converted_text')}"
    "[DATA]\n{data}\n[/DATA]"
)