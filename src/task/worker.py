from celery import Celery
from ai.LLMService import LLMService
from data.VulnerabilityReport import create_from_flama_json
import models.models as db_models
from my_db import Session
from dotenv import load_dotenv
import os

load_dotenv()
llm_service = LLMService()


redis_url = os.getenv("REDIS_ENDPOINT")

worker = Celery(
    'worker',
    broker=redis_url,
    backend=redis_url
)

def fun(self, exc, task_id, args, kwargs, einfo):
    print('Failed!')

@worker.task(name="worker.generate_report",on_failure=fun)
def generate_report(recommendation_task_id: int):
    
    if recommendation_task_id is None:
        print("recommendation_task_id is None")
        return
    print("recommendation_task_id", recommendation_task_id)
    with Session() as session:
        findings_from_db = session.query(db_models.Finding).join(db_models.RecommendationTask).filter(db_models.RecommendationTask.id==recommendation_task_id).limit(10).all()
        
        if(not findings_from_db):
            print("No findings found")
            return
        print("llm_service", llm_service)
        findings= [f.raw_data for f in findings_from_db]
        finding_ids = [f.id for f in findings_from_db]
    vulnerability_report  = create_from_flama_json(findings,n=1, llm_service=llm_service)
    vulnerability_report.add_category()
    vulnerability_report.add_solution()
    
    with Session() as session:
        for finding_id, f in zip(finding_ids, vulnerability_report.findings):
            finding = session.query(db_models.Finding).filter(db_models.Finding.id==finding_id).first()
            if finding is None:
                print(f"Finding with id {finding_id} not found")
                continue
            recommendation = db_models.Recommendation(
                description_short=f.solution.short_description if f.solution.short_description else "No short description",
                description_long=f.solution.long_description if f.solution.long_description else "No long description",
                meta= f.solution.metadata if f.solution.metadata else {},
                search_terms= f.solution.search_terms if f.solution.search_terms else [],
                finding_id=finding_id,
                recommendation_task_id=recommendation_task_id
            )
            session.add(recommendation)
            ## updat recommendation task status
            recommendation_task = session.query(db_models.RecommendationTask).filter(db_models.RecommendationTask.id==recommendation_task_id).first()
            recommendation_task.status = db_models.TaskStatus.COMPLETED
        session.commit()
