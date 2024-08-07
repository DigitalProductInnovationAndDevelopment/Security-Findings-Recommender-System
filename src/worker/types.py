from pydantic import BaseModel


class GenerateReportInput(BaseModel):
    recommendation_task_id: int
    generate_long_solution: bool = True
    generate_search_terms: bool = True
    generate_aggregate_solutions: bool = True
