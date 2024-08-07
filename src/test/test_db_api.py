import json
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from data.AggregatedSolution import AggregatedSolution
from data.Solution import Solution
from data.types import Content
from sqlalchemy.orm.session import Session

from data.Finding import Finding
import db.models as db_models
from repository.finding import FindingRepository, get_finding_repository
from repository.recommendation import (
    RecommendationRepository,
    get_recommendation_repository,
)
from repository.task import TaskRepository, get_task_repository
from app import app
from repository.types import (
    AggregatedSolutionInput,
    CreateAggregatedRecommendationInput,
)

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


db_models.BaseModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_task_repository(session: Session = Depends(override_get_db)):
    return TaskRepository(session)


def override_get_finding_repository(session: Session = Depends(override_get_db)):
    return FindingRepository(session)


def override_get_recommendation_repository(session: Session = Depends(override_get_db)):
    return RecommendationRepository(session)


app.dependency_overrides[get_task_repository] = override_get_task_repository
app.dependency_overrides[get_finding_repository] = override_get_finding_repository
app.dependency_overrides[get_recommendation_repository] = (
    override_get_recommendation_repository
)


client = TestClient(app)


def generate_findings():
    return [
        {
            "doc_type": "summary",
            "criticality_tag": ["unrestricted", 0],
            "knowledge_type": "derived",
            "requirement_list": [""],
            "title_list": [
                {
                    "element": "finding_title_" + str(x),
                    "source": "Trivy",
                }
            ],
            "location_list": [],
            "description_list": [
                {
                    "element": "finding_description_" + str(x),
                    "source": "Trivy",
                }
            ],
            "internal_rating_list": [],
            "internal_ratingsource_list": [],
            "cvss_rating_list": [],
            "rule_list": [],
            "cwe_id_list": [],
            "cve_id_list": [],
            "activity_list": [],
            "first_found": "2023-08-24T08:32:33+00:00",
            "last_found": "2023-08-25T15:48:01+00:00",
            "report_amount": 4,
            "content_hash": "",
            "severity": x * 10,
            "severity_explanation": "",
            "priority": x * 10,
            "priority_explanation": "",
            "sum_id": "",
            "prio_id": "",
            "element_tag": "",
        }
        for x in range(10)
    ]


def test_create_get_task_integration():

    with TestingSessionLocal() as session:
        task_repo = TaskRepository(session=session)
        task = task_repo.create_task()
        task_repo.get_task_by_id

    response = client.get(
        "api/v1/tasks/",
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_processing_recommendation():

    with TestingSessionLocal() as session:
        create_task = TaskRepository(session=session)
        task = create_task.create_task()

    response = client.post(
        "api/v1/recommendations/", json={"filter": {"task_id": task.id}}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Recommendation task is still processing"


def test_recommendation_done():
    with TestingSessionLocal() as session:
        repo = TaskRepository(session=session)
        task = repo.create_task()
        repo.update_task_completed(task.id)

        response = client.post(
            "api/v1/recommendations/", json={"filter": {"task_id": task.id}}
        )
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 0


def test_recommendation_with_findings_and_solution():
    with TestingSessionLocal() as session:
        repo = TaskRepository(session=session)
        task = repo.create_task()
        repo.update_task_completed(task.id)
        findings = generate_findings()

        findings_db = [
            db_models.Finding().from_data(
                Content.model_validate_json(json.dumps(finding))
            )
            for finding in findings
        ]

        findingRepo = FindingRepository(session=session)
        for finding in findings_db:
            finding.recommendation_task_id = task.id

        findingRepo.create_findings(findings_db)

        # refresh finding ids
        for finding in findings_db:
            session.refresh(finding)

        recommendationRepo = RecommendationRepository(session=session)
        recommendationRepo.create_recommendations(
            list(
                zip(
                    [finding.id for finding in findings_db],
                    [
                        Finding(
                            solution=Solution(
                                short_description="short_description",
                                long_description="long_description",
                            )
                        )
                        for _ in findings_db
                    ],
                )
            ),
            recommendation_task_id=task.id,
        )

        response = client.post(
            "api/v1/recommendations/", json={"filter": {"task_id": task.id}}
        )
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 10

        assert "solution" in response.json()["items"][0]

        assert "short_description" in response.json()["items"][0]["solution"]
        assert "long_description" in response.json()["items"][0]["solution"]


def test_recommendation_with_findings_filter():
    with TestingSessionLocal() as session:
        repo = TaskRepository(session=session)
        task = repo.create_task()
        repo.update_task_completed(task.id)
        findings = generate_findings()

        findings_db = [
            db_models.Finding().from_data(
                Content.model_validate_json(json.dumps(finding))
            )
            for finding in findings
        ]
        findingRepo = FindingRepository(session=session)
        for finding in findings_db:
            finding.recommendation_task_id = task.id

        findingRepo.create_findings(findings_db)

        response = client.post(
            "api/v1/recommendations/",
            json={
                "filter": {
                    "task_id": task.id,
                },
                "pagination": {"limit": 5, "offset": 0},
            },
        )
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 5

        response = client.post(
            "api/v1/recommendations/",
            json={
                "filter": {
                    "task_id": task.id,
                    "severity": {"minValue": 10, "maxValue": 20},
                },
                "pagination": {"limit": 5, "offset": 0},
            },
        )
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 2


def test_aggregated_solutions_response():
    with TestingSessionLocal() as session:
        repo = TaskRepository(session=session)
        task = repo.create_task()
        repo.update_task_completed(task.id)
        findings = generate_findings()
        findings_db = [
            db_models.Finding().from_data(
                Content.model_validate_json(json.dumps(finding))
            )
            for finding in findings
        ]
        findingRepo = FindingRepository(session=session)
        for finding in findings_db:
            finding.recommendation_task_id = task.id

        findingRepo.create_findings(findings_db)

        for finding in findings_db:
            session.refresh(finding)

        recommendationRepo = RecommendationRepository(session=session)

        recommendationRepo.create_aggregated_solutions(
            input=CreateAggregatedRecommendationInput(
                aggregated_solutions=[
                    AggregatedSolutionInput(
                        solution=AggregatedSolution(
                            findings=[],
                            solution="Aggregated Solution",
                            metadata={"meta": "data"},
                        ),
                        findings_db_ids=[finding.id for finding in findings_db],
                    )
                ],
                recommendation_task_id=task.id,
            )
        )
        # TODO: test based on date. Doesn't work for now with sqlite
        response = client.post(
            "api/v1/recommendations/aggregated/",
            json={
                "filter": {
                    "task_id": task.id,
                },
            },
        )
        print(response.json())
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 1

        assert "solution" in response.json()["items"][0]
        assert "findings" in response.json()["items"][0]

        # check if aggregated respionse has a correct solution
        assert response.json()["items"][0]["solution"] == "Aggregated Solution"
        assert len(response.json()["items"][0]["findings"]) == 10

        # check if the format is correct
        assert all(
            [
                "finding_title_" in finding["title"][0]
                for finding in response.json()["items"][0]["findings"]
            ]
        )
