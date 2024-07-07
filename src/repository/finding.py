from sqlalchemy import Date, cast
from data.pagination import PaginationInput
import db.models as db_models

from sqlalchemy.orm import Session
from fastapi import Depends
from db.my_db import get_db


class FindingRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_findings(self, num_findings: int) -> list[db_models.Finding]:
        findings = self.session.query(db_models.Finding).limit(num_findings).all()
        return findings

    def get_findings_by_task_id(
        self, task_id: int, pagination: PaginationInput
    ) -> list[db_models.Finding]:
        findings = (
            self.session.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .where(
                db_models.RecommendationTask.status == db_models.TaskStatus.COMPLETED,
                (db_models.RecommendationTask.id == task_id),
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
            .all()
        )

        return findings

    def get_findings_count_by_task_id(self, task_id: int) -> int:
        count = (
            self.session.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .where(
                db_models.RecommendationTask.status == db_models.TaskStatus.COMPLETED,
                (db_models.RecommendationTask.id == task_id),
            )
            .count()
        )

        return count

    def create_findings(
        self, findings: list[db_models.Finding]
    ) -> list[db_models.Finding]:
        self.session.bulk_save_objects(findings)
        self.session.commit()


def get_finding_repository(session: Depends = Depends(get_db)):
    return FindingRepository(session)
