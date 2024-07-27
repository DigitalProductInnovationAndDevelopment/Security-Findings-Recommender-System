from fastapi import Depends

from sqlalchemy import Date, Integer, cast, func
from sqlalchemy.orm import Session

import db.models as db_models
from data.apischema import SeverityFilter
from data.pagination import PaginationInput
from db.my_db import get_db
from repository.types import GetFindingsByFilterInput


class FindingRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_findings(self, num_findings: int) -> list[db_models.Finding]:
        findings = self.session.query(db_models.Finding).limit(num_findings).all()
        return findings

    def get_all_findings_by_task_id_for_processing(self, task_id: int, limit: int = -1):
        query = (
            self.session.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .filter(db_models.RecommendationTask.id == task_id)
        )

        # Remove Limit For Now
        if limit > 0:
            query = query.limit(limit)

        return query.all()

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

    def get_findings_by_task_id_and_filter(
        self, input: GetFindingsByFilterInput
    ) -> list[db_models.Finding]:
        task_id = input.task_id
        pagination = input.pagination
        severity = input.severityFilter
        query = (
            self.session.query(db_models.Finding)
            .join(db_models.RecommendationTask)
            .where(
                db_models.RecommendationTask.status == db_models.TaskStatus.COMPLETED,
                (db_models.RecommendationTask.id == task_id),
                (
                    db_models.Finding.severity >= severity.minValue
                    if severity and severity.minValue
                    else True
                ),
                (
                    db_models.Finding.severity <= severity.maxValue
                    if severity and severity.maxValue
                    else True
                ),
            )
        )

        total = query.count()
        findings = query.all()
        if pagination:
            query = query.offset(pagination.offset).limit(pagination.limit)

        return findings, total

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


def get_finding_repository(session: Session = Depends(get_db)):
    return FindingRepository(session)
