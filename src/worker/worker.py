from celery import Celery
from ai.LLM.Strategies.OLLAMAService import OLLAMAService
from ai.LLM.LLMServiceStrategy import LLMServiceStrategy
from data.VulnerabilityReport import create_from_flama_json
import db.models as db_models
from db.my_db import Session
import logging

logger = logging.getLogger(__name__)

from config import config

my_strategy = OLLAMAService()
llm_service = LLMServiceStrategy(my_strategy)


redis_url = config.redis_endpoint

print(f"Redis URL: {redis_url}")
limit = int(config.queue_processing_limit)  # default limit is 5 , -1 means no limit


worker = Celery("worker", broker=redis_url, backend=redis_url)


print(f"Worker: {worker}")


def error(self, exc, task_id, args, kwargs, einfo):
    logger.error(f"Task {task_id} raised exception: {exc}")


@worker.task(name="worker.generate_report", on_failure=error)
def generate_report(recommendation_task_id: int, stragegy: str = "OLLAMA"):

    if recommendation_task_id is None:
        logger.warning("Recommendation task id is None")
        return
    logger.info(f"Processing recommendation task with id {recommendation_task_id}")
    logger.info(f"Processing recommendation task with limit {limit}")
    logger.info(
        f"Processing recommendation task with model_name {my_strategy.model_name}"
    )
    with Session() as session:
        query = (
            session.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .filter(db_models.RecommendationTask.id == recommendation_task_id)
        )
        if limit > 0:
            query = query.limit(limit)

        findings_from_db = query.all()
        logger.info(f"Found {len(findings_from_db)} findings for recommendation task")
        if not findings_from_db:
            logger.warn(
                f"No findings found for recommendation task {recommendation_task_id}"
            )
            return

        findings = [f.raw_data for f in findings_from_db]
        finding_ids = [f.id for f in findings_from_db]
    vulnerability_report = create_from_flama_json(
        findings, n=limit, llm_service=llm_service
    )
    vulnerability_report.add_category()
    vulnerability_report.add_solution()

    with Session() as session:
        for finding_id, f in zip(finding_ids, vulnerability_report.findings):
            finding = (
                session.query(db_models.Finding)
                .filter(db_models.Finding.id == finding_id)
                .first()
            )
            if finding is None:
                print(f"Finding with id {finding_id} not found")
                continue
            recommendation = db_models.Recommendation(
                description_short=(
                    f.solution.short_description
                    if f.solution.short_description
                    else "No short description"
                ),
                description_long=(
                    f.solution.long_description
                    if f.solution.long_description
                    else "No long description"
                ),
                meta=f.solution.metadata if f.solution.metadata else {},
                search_terms=f.solution.search_terms if f.solution.search_terms else [],
                finding_id=finding_id,
                recommendation_task_id=recommendation_task_id,
                # TODO: fix category changes
                category=f.category.affected_component.value if f.category else None,
            )
            session.add(recommendation)
            ## updat recommendation task status
            recommendation_task = (
                session.query(db_models.RecommendationTask)
                .filter(db_models.RecommendationTask.id == recommendation_task_id)
                .first()
            )
            recommendation_task.status = db_models.TaskStatus.COMPLETED
        session.commit()
