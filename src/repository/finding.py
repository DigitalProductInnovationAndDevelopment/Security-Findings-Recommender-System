import db.models as db_models

from sqlalchemy.orm import Session


class FindingRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_findings(self, num_findings: int) -> list[db_models.Finding]:
        with self.session as session:
            findings = session.query(db_models.Finding).limit(num_findings).all()
            return findings
