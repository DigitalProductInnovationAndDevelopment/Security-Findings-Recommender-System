from typing import List

from tqdm import tqdm

from ai.Grouping.FindingBatcher import FindingBatcher
from ai.LLM.BaseLLMService import BaseLLMService
from data.AggregatedSolution import AggregatedSolution
from data.VulnerabilityReport import VulnerabilityReport


class FindingGrouper:
    def __init__(
        self, vulnerability_report: VulnerabilityReport, llm_service: BaseLLMService
    ):
        self.vulnerability_report = vulnerability_report
        self.llm_service = llm_service
        self.batcher = FindingBatcher(llm_service)
        self.batches = self.batcher.create_batches(vulnerability_report.get_findings())
        self.aggregated_solutions: List[AggregatedSolution] = []

    def generate_aggregated_solutions(self):
        for batch in tqdm(self.batches, desc="Generating Aggregated Solutions"):
            result_list = self.llm_service.generate_aggregated_solution(batch)
            for result in result_list:
                self.aggregated_solutions.append(
                    AggregatedSolution().from_result(result[1], result[0], result[2])
                )  # Solution, Findings, Metadata
        self.vulnerability_report.set_aggregated_solutions(self.aggregated_solutions)
