from .base import Column, BaseModel

from typing import List, Optional
from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship


class Recommendation(BaseModel):
    __tablename__ = "recommendations"
    recommendation: str = Column(String, nullable=False)
    generic: bool = Column(String, default=False, nullable=False)
    finding_id: int = Column(Integer, ForeignKey("findings.id"), nullable=True)
    finding: Mapped[Optional['Finding']] = relationship('Finding', uselist=False, back_populates='recommendations')

    def __repr__(self):
        return f"<Recommendation {self.recommendation}>"


class Finding(BaseModel):
    __tablename__ = "findings"
    finding = Column(String, default=None, nullable=True)
    cve = Column(String, default=None, nullable=True)
    priority = Column(String, default=None, nullable=True)
    source = Column(String, default=None, nullable=True)
    content = Column(JSON, default=None, nullable=False)
    # recommendations: list["Recommendation"] = Relationship(back_populates="finding")
    recommendations: Mapped[List['Recommendation']] = relationship('Recommendation', back_populates='finding')

    def __init__(self, finding: str, content: JSON):
        self.content = content

    def __repr__(self):
        return f"<Finding {self.finding}>"


class User(BaseModel):
    __tablename__ = "users"
    external_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    preferences = Column(String, nullable=True)
