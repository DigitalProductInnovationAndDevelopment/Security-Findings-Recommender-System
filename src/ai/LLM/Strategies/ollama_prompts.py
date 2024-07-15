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

SUBDIVISION_PROMPT_TEMPLATE = (
    "You are a cybersecurity expert tasked with grouping related security findings. "
    "Analyze the following list of findings and group them based on their relationships or common themes. "
    "For each group, provide a brief reason for grouping them together.\n\n"
    "Provide your answer in the following JSON format:\n"
    '{{"subdivisions": [\n'
    '  {{"group": "<comma-separated list of finding numbers, e.g. 3,4,5,8>", "reason": "<brief reason for grouping>"}}\n'
    ']}}\n\n'
    "Findings:\n{data}"
)

AGGREGATED_SOLUTION_TEMPLATE = (
    "As a senior cybersecurity strategist, your task is to provide a high-level, strategic solution for a group of related security findings. "
    "Your goal is to synthesize the information and create a broad, actionable recommendation that addresses the root causes of multiple issues.\n\n"
    "Group meta information: {meta_info}\n\n"
    "Instructions:\n"
    "1. Review the group of findings provided at the end of this prompt.\n"
    "2. Identify common themes or root causes among the findings.\n"
    "3. Generate a strategic, overarching solution that addresses these core issues.\n"
    "4. Your solution should be:\n"
    "   - High-level: Focus on broad strategies rather than specific technical fixes\n"
    "   - Widely applicable: Address multiple findings with each recommendation\n"
    "   - Proactive: Aim to prevent similar issues in the future\n"
    "   - Actionable: Provide clear, general steps for implementation\n"
    "   - Concise: Use clear and precise language\n\n"
    "Your response should be structured as follows:\n"
    "1. Summary: A brief overview of the core security challenges (1-2 sentences)\n"
    "2. Strategic Solution: A high-level approach to address the underlying issues (3-5 key points)\n"
    "3. Implementation Guidance: General steps for putting the strategy into action\n"
    "4. Long-term Considerations: Suggestions for ongoing improvement and risk mitigation\n\n"
    "You may use Markdown formatting in your response to improve readability.\n"
    f"{answer_in_json_prompt('aggregated_solution')}"
    "Findings:\n{data}"
)

CONVERT_DICT_TO_STR_TEMPLATE = (
    "You are a data formatting expert. Convert the following dictionary into a human-readable string. "
    f"{answer_in_json_prompt('converted_text')}"
    "[DATA]\n{data}\n[/DATA]"
)
