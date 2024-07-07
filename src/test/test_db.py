from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sqlalchemy.orm.session import Session

import db.models as db_models
from repository.finding import FindingRepository, get_finding_repository
from repository.recommendation import (
    RecommendationRepository,
    get_recommendation_repository,
)
from repository.task import TaskRepository, get_task_repository
from app import app

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


def test_create_get_task_integration():

    with TestingSessionLocal() as session:
        task_repo = TaskRepository(session=session)
        task = task_repo.create_task()
        task_repo.get_task_by_id

    response = client.get(
        "tasks/",
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
