# This tests the interworkings of the LLMServiceStrategy, VulnerabilityReport, and Finding classes.

from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
from data.Finding import Finding
from data.VulnerabilityReport import VulnerabilityReport

from .mock_llm import MockLLMService


# Test the LLMServiceStrategy together with VulnerabilityReport and Finding
def setup():
    llm = LLMServiceStrategy(MockLLMService())
    report = VulnerabilityReport()
    oneFinding = Finding(
        title=["title1", "title2"], descriptions=["description1", "description2"]
    )
    oneFinding._llm_service = llm
    report.add_finding(oneFinding)

    return llm, report, oneFinding


llm, report, oneFinding = setup()


def test_llm_setup():
    oneFinding.combine_descriptions()
    assert oneFinding.description == "combined_description"

    assert report.findings[0].solution == None


def test_solution_short_generation():
    report.add_solution(short=True, long=False)
    assert report.findings[0].solution.short_description == "recommendation_response"
    assert report.findings[0].solution.long_description == None


def test_solution_long_generation():
    report.add_solution(short=False, long=True)
    assert report.findings[0].solution.short_description == None
    assert report.findings[0].solution.long_description == "recommendation_response"


def test_solution_short_long_generation():
    report.add_solution(short=True, long=True)
    assert report.findings[0].solution.short_description == "recommendation_response"
    assert report.findings[0].solution.long_description == "recommendation_response"


def test_solution_search_terms_generation():
    report.add_solution(short=True, long=True)
    assert report.findings[0].solution.search_terms == "search_terms_response"


def test_classification():
    report.add_category()
    assert report.findings[0].category.technology_stack.value == "JavaScript"
