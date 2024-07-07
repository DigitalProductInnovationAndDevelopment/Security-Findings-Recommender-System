import db.models as db_models

from sqlalchemy.orm import Session, sessionmaker


from db.my_db import get_db
from fastapi import Depends


class RecommendationRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_recommendations(
        self, num_recommendations: int
    ) -> list[db_models.Recommendation]:

        recommendations = (
            self.session.query(db_models.Recommendation)
            .limit(num_recommendations)
            .all()
        )
        return recommendations

    def get_recommendation_by_id(
        self, recommendation_id: int
    ) -> db_models.Recommendation:

        recommendation = self.session.query(db_models.Recommendation).get(
            recommendation_id
        )
        return recommendation


def get_recommendation_repository(session: Session = Depends(get_db)):
    return RecommendationRepository(session)
