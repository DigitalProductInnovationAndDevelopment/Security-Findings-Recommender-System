import db.models as db_models

from sqlalchemy.orm import Session


class TaskRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_tasks(self, num_recommendations: int) -> list[db_models.RecommendationTask]:
        with self.session as session:
            tasks = (
                session.query(db_models.RecommendationTask)
                .limit(num_recommendations)
                .all()
            )
            return tasks

    def get_task_by_id(self, task_id: int) -> db_models.RecommendationTask:
        with self.session as session:
            task = session.query(db_models.RecommendationTask).get(task_id)
            return task
