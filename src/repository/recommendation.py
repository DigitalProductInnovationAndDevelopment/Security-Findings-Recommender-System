import db.models as db_models

from sqlalchemy.orm import Session


class RecommendationRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_recommendations(
        self, num_recommendations: int
    ) -> list[db_models.Recommendation]:
        with self.session as session:
            recommendations = (
                session.query(db_models.Recommendation).limit(num_recommendations).all()
            )
            return recommendations
