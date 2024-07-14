import re
from config import config


def estimate_tokens(text):
    """
    Estimate the number of tokens in a given text.

    This function provides a conservative estimate of the number of tokens
    in a text, without using a specific tokenizer. It's designed to slightly
    overestimate to ensure the text fits within an LLM's context window.

    The estimation is based on the following rules:
    - Words of 1-2 characters are counted as 1 token
    - Words of 3-5 characters are counted as 2 tokens
    - Words of 6-10 characters are counted as 3 tokens
    - Words longer than 10 characters are counted as 1 token per 4 characters + 1
    - Each punctuation mark and space is counted as an additional token
    - A 10% buffer is added to the final count

    Args:
    text (str): The input text to estimate tokens for.

    Returns:
    int: The estimated number of tokens in the text.
    """
    # Remove punctuation and split the text into words
    words = re.findall(r'\w+', text.lower())

    total_tokens = 0
    for word in words:
        # Estimate tokens based on word length
        if len(word) <= 2:
            total_tokens += 1
        elif len(word) <= 5:
            total_tokens += 2
        elif len(word) <= 10:
            total_tokens += 3
        else:
            # For very long words: 1 token per 4 characters + 1 extra
            total_tokens += (len(word) // 4) + 1

    # Add extra tokens for punctuation and spaces
    total_tokens += len(re.findall(r'[^\w\s]', text))
    total_tokens += text.count(' ')

    # Add a 10% buffer to err on the side of caution
    total_tokens = int(total_tokens * 1.1)

    return total_tokens


def fits_in_context(text):
    """
    Check if the given text fits within the maximum context size.

    This function estimates the number of tokens in the text and compares
    it to the MAX_CONTEXT value imported from config.py.

    Args:
    text (str): The input text to check.

    Returns:
    bool: True if the text fits within the context, False otherwise.
    """
    estimated_tokens = estimate_tokens(text)
    return estimated_tokens <= config.max_context_length


# Example usage
if __name__ == "__main__":
    sample_text = "This is a sample text to estimate the number of tokens in a sentence."
    estimated_tokens = estimate_tokens(sample_text)
    print(f"Estimated number of tokens: {estimated_tokens}")

    if fits_in_context(sample_text):
        print("The text fits within the maximum context.")
    else:
        print("The text exceeds the maximum context size.")