from sqlalchemy import Date, cast
import db.models as db_models

from sqlalchemy.orm import Session

from db.my_db import get_db
from fastapi import Depends


class TaskRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def create_task(self) -> db_models.RecommendationTask:

        task = db_models.RecommendationTask()
        self.session.add(task)
        self.session.commit()
        self.session.flush()
        self.session.refresh(task)
        return task

    def update_task(self, task: db_models.RecommendationTask, celery_task_id: str):
        task.celery_task_id = celery_task_id
        self.session.commit()
        self.session.flush()
        self.session.refresh(task)
        return task

    def get_tasks(
        self,
    ) -> list[db_models.RecommendationTask]:

        tasks = self.session.query(db_models.RecommendationTask).all()
        return tasks

    def get_task_by_id(self, task_id: int) -> db_models.RecommendationTask | None:

        task = (
            self.session.query(db_models.RecommendationTask)
            .where(db_models.RecommendationTask.id == task_id)
            .first()
        )

        return task

    def get_task_by_date(self, date: Date) -> db_models.RecommendationTask | None:

        task = (
            self.session.query(db_models.RecommendationTask)
            .filter(cast(db_models.RecommendationTask.created_at, Date) == date)
            .order_by(db_models.RecommendationTask.created_at)
            .first()
        )
        return task

    def delete_all_tasks(self):
        count = self.session.query(db_models.RecommendationTask).delete()
        self.session.commit()
        return count

    def delete_task(self, task: db_models.RecommendationTask):
        if task:
            self.session.delete(task)
        self.session.commit()


def get_task_repository(session: Session = Depends(get_db)):
    return TaskRepository(session)
