from .base import Column, BaseModel

from typing import List, Optional
from sqlalchemy import JSON, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, relationship
from enum import Enum as PyEnum


from data.types import Content


class Recommendation(BaseModel):
    __tablename__ = "recommendations"
    description_short = Column(String, nullable=True)
    description_long = Column(String, nullable=True)
    search_terms = Column(String, nullable=True)
    meta = Column(JSON, default={}, nullable=True)
    category = Column(String, nullable=True)
    finding_id: int = Column(Integer, ForeignKey("findings.id"), nullable=True)
    recommendation_task_id = Column(
        Integer,
        ForeignKey("recommendation_task.id", ondelete="CASCADE"),
        nullable=False,
    )
    finding: Mapped[Optional["Finding"]] = relationship(
        "Finding", uselist=False, back_populates="recommendations"
    )

    def __repr__(self):
        return f"<Recommendation {self.recommendation}>"


class Finding(BaseModel):
    __tablename__ = "findings"
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    title_list = Column(JSON, default=None, nullable=True)
    description_list = Column(JSON, default=[], nullable=True)
    locations_list = Column(JSON, default=[], nullable=True)
    cwe_id_list = Column(JSON, default=[], nullable=True)
    cve_id_list = Column(JSON, default=[], nullable=True)
    priority = Column(String, default=None, nullable=True)
    severity = Column(String, default=None, nullable=True)
    language = Column(String, default=None, nullable=True)
    source = Column(String, default=None, nullable=True)  #
    report_amount = Column(Integer, default=1, nullable=False)
    raw_data = Column(JSON, default=None, nullable=True)

    ## makes sure we have a task to map to, used for creating one request per day.
    recommendation_task_id = Column(
        Integer,
        ForeignKey("recommendation_task.id", ondelete="CASCADE"),
        nullable=False,
    )
    recommendation_task: Mapped[Optional["RecommendationTask"]] = relationship(
        "RecommendationTask", uselist=False, back_populates="findings"
    )

    # recommendations: list["Recommendation"] = Relationship(back_populates="finding")
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="finding"
    )

    def from_data(self, data: Content):
        self.cve_id_list = (
            [x.dict() for x in data.cve_id_list] if data.cve_id_list else []
        )
        self.description_list = (
            [x.dict() for x in data.description_list] if data.description_list else []
        )
        self.title_list = [x.dict() for x in data.title_list]
        self.locations_list = (
            [x.dict() for x in data.location_list] if data.location_list else []
        )
        self.raw_data = data.dict()
        self.report_amount = data.report_amount
        return self

    def __repr__(self):
        return f"<Finding {self.finding}>"


class User(BaseModel):
    __tablename__ = "users"
    external_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    preferences = Column(String, nullable=True)


class TaskStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class RecommendationTask(BaseModel):
    __tablename__ = "recommendation_task"
    status: TaskStatus = Column(
        Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )
    celery_task_id = Column(String, nullable=True)
    findings: Mapped[List[Finding]] = relationship(
        "Finding", back_populates="recommendation_task", passive_deletes=True
    )
