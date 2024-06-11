import requests
import re
import os

def get_github_advisory_by_cve(cve_id):
    """
    Fetches GitHub advisory using the CVE ID and GitHub token from environment variables.

    Parameters:
    cve_id (str): The CVE ID to fetch the advisory for.

    Returns:
    dict or None: The advisory data if the request is successful, otherwise None.
    """
    # Validate the CVE ID format
    cve_pattern = re.compile(r'^CVE-\d{4}-\d{4,}$')
    if not cve_pattern.match(cve_id):
        raise ValueError("Invalid CVE ID format. Format should be 'CVE-YYYY-NNNN'.")

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token not found in environment variables")

    url = f"https://api.github.com/advisories/{cve_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    
    return None