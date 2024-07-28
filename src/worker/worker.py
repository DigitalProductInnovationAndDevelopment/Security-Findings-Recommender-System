import logging

from celery import Celery
from celery.signals import worker_init

import db.models as db_models

from db.my_db import engine, sessionmaker
from repository.finding import FindingRepository
from repository.recommendation import RecommendationRepository
from repository.task import TaskRepository
from repository.types import (
    AggregatedSolutionInput,
    CreateAggregatedRecommendationInput,
)


from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
from ai.LLM.Strategies.OLLAMAService import OLLAMAService
from data.VulnerabilityReport import create_from_flama_json
from ai.Grouping.FindingGrouper import FindingGrouper


logger = logging.getLogger(__name__)

from config import config

Session = sessionmaker(engine)
redis_url = config.redis_endpoint

print(f"Redis URL: {redis_url}")
limit = int(config.queue_processing_limit)  # default limit is 5 , -1 means no limit


worker = Celery("worker", broker=redis_url, backend=redis_url)


def error(self, exc, task_id, args, kwargs, einfo):
    logger.error(f"Task {task_id} raised exception: {exc}")


@worker.task(name="worker.generate_report", on_failure=error)
def generate_report(
    recommendation_task_id: int,
    generate_long_solution: bool = True,
    generate_search_terms: bool = True,
    generate_aggregate_solutions: bool = True,
):

    # importing here so importing worker does not import all the dependencies
    # from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
    # from ai.LLM.Strategies.OLLAMAService import OLLAMAService
    # from data.VulnerabilityReport import create_from_flama_json

    ollama_strategy = OLLAMAService()
    llm_service = LLMServiceStrategy(ollama_strategy)

    logger.info(f"Processing recommendation task with id {recommendation_task_id}")
    logger.info(f"Processing recommendation task with limit {limit}")
    logger.info(
        f"long: {generate_long_solution}, search: {generate_search_terms}, aggregate: {generate_aggregate_solutions}"
    )

    recommendationTask = None
    try:
        with Session() as session:

            taskRepo = TaskRepository(session)
            recommendationTask = taskRepo.get_task_by_id(recommendation_task_id)

            if not recommendationTask:
                logger.error(
                    f"Recommendation task with id {recommendation_task_id} not found"
                )
                return
            find_repo = FindingRepository(session)
            findings_from_db = find_repo.get_all_findings_by_task_id_for_processing(
                recommendation_task_id, limit
            )

            logger.info(
                f"Found {len(findings_from_db)} findings for recommendation task"
            )
            if not findings_from_db:
                logger.warn(
                    f"No findings found for recommendation task {recommendation_task_id}"
                )
                return

            findings = [f.raw_data for f in findings_from_db]
            finding_ids = [f.id for f in findings_from_db]

    except Exception as e:
        logger.error(f"Error processing recommendation task: {e}")
        return

    vulnerability_report = create_from_flama_json(
        findings,
        n=limit,
        llm_service=llm_service,
        shuffle_data=False,  # set it true may cause zip to work incorrectly
    )

    # map findings to db ids, used for aggregated solutions
    finding_id_map = {
        finding.id: db_id
        for db_id, finding in zip(finding_ids, vulnerability_report.findings)
    }

    vulnerability_report.add_category()
    vulnerability_report.add_solution(
        search_term=generate_search_terms, long=generate_long_solution
    )

    if generate_aggregate_solutions:
        # after all the findings are processed, we need to group them

        findingGrouper = FindingGrouper(vulnerability_report, ollama_strategy)
        findingGrouper.generate_aggregated_solutions()
        # map findings to db ids for aggregated solutions
        aggregated_solutions_with_db_ids = [
            AggregatedSolutionInput(
                findings_db_ids=[
                    finding_id_map[finding.id] for finding in solution.findings
                ],
                solution=solution,
            )
            for solution in vulnerability_report.aggregated_solutions
        ]
    with Session() as session:
        recommendationRepo = RecommendationRepository(session)
        recommendationRepo.create_recommendations(
            list(zip(finding_ids, vulnerability_report.findings)),
            recommendation_task_id,
        )

        if generate_aggregate_solutions:
            # save aggregated solutions
            recommendationRepo = RecommendationRepository(session)
            recommendationRepo.create_aggregated_solutions(
                input=CreateAggregatedRecommendationInput(
                    aggregated_solutions=aggregated_solutions_with_db_ids,
                    recommendation_task_id=recommendation_task_id,
                )
            )
        # finally update the task status
        recommendationRepo = TaskRepository(session)
        recommendationRepo.update_task_completed(recommendation_task_id)
