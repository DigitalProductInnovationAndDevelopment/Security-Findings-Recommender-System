from data.Finding import Finding
import db.models as db_models

from sqlalchemy.orm import Session, sessionmaker


from db.my_db import get_db
from fastapi import Depends

from repository.types import CreateAggregatedRecommendationInput


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

    def create_recommendations(
        self,
        finding_with_solution: list[tuple[str, Finding]],
        recommendation_task_id: int,
    ):
        session = self.session
        for finding_id, f in finding_with_solution:
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
                    else "No short description available"
                ),
                description_long=(
                    f.solution.long_description
                    if f.solution.long_description
                    else "No long description available"
                ),
                meta=f.solution.metadata if f.solution.metadata else {},
                search_terms=f.solution.search_terms if f.solution.search_terms else "",
                finding_id=finding_id,
                recommendation_task_id=recommendation_task_id,
                category=(f.category.model_dump_json() if f.category else None),
            )
            session.add(recommendation)
            ## update recommendation task status

        session.commit()

    def create_aggregated_solutions(
        self,
        input: CreateAggregatedRecommendationInput,
    ):

        for solution in input.aggregated_solutions:
            aggregated_rec = db_models.AggregatedRecommendation(
                solution=solution.solution.solution,
                meta=solution.solution.metadata,
                recommendation_task_id=input.recommendation_task_id,
            )
            self.session.add(aggregated_rec)
            self.session.commit()
            self.session.refresh(aggregated_rec)
            for findings_id in solution.findings_db_ids:

                res = self.session.execute(
                    db_models.findings_aggregated_association_table.insert().values(
                        finding_id=findings_id,
                        aggregated_recommendation_id=aggregated_rec.id,
                    )
                )
                res.close()

        self.session.commit()

    def get_aggregated_solutions(
        self, recommendation_task_id: int
    ) -> list[db_models.AggregatedRecommendation]:

        aggregated_solutions = (
            self.session.query(db_models.AggregatedRecommendation)
            .filter(
                db_models.AggregatedRecommendation.recommendation_task_id
                == recommendation_task_id
            )
            .all()
        )
        return aggregated_solutions


def get_recommendation_repository(session: Session = Depends(get_db)):
    return RecommendationRepository(session)
