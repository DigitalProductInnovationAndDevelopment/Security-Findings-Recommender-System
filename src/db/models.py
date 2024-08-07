from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

from data.types import Content

from .base import BaseModel, Column


findings_aggregated_association_table = Table(
    "findings_aggregated_association",
    BaseModel.metadata,
    Column(
        "finding_id",
        ForeignKey("findings.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "aggregated_recommendation_id",
        ForeignKey("aggregated_recommendations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Recommendation(BaseModel):
    __tablename__ = "recommendations"
    description_short = Column(String, nullable=True)
    description_long = Column(String, nullable=True)
    search_terms = Column(String, nullable=True)
    meta = Column(JSON, default={}, nullable=True)
    category = Column(JSON, nullable=True)
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
        return f"<Recommendation {self.description_short}>"


class AggregatedRecommendation(BaseModel):
    __tablename__ = "aggregated_recommendations"
    solution = Column(String, nullable=True)
    meta = Column(JSON, default={}, nullable=True)
    recommendation_task_id = Column(
        Integer,
        ForeignKey("recommendation_task.id", ondelete="CASCADE"),
        nullable=False,
    )
    findings: Mapped[List["Finding"]] = relationship(
        secondary=findings_aggregated_association_table,
        back_populates="aggregated_recommendations",
    )

    def __repr__(self):
        return f"<Aggregated Recommendation {self.solution}>"


class Finding(BaseModel):
    __tablename__ = "findings"
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    title_list = Column(JSON, default=None, nullable=True)
    description_list = Column(JSON, default=[], nullable=True)
    locations_list = Column(JSON, default=[], nullable=True)
    category = Column(JSON, nullable=True)
    cwe_id_list = Column(JSON, default=[], nullable=True)
    cve_id_list = Column(JSON, default=[], nullable=True)
    priority = Column(Integer, default=None, nullable=True)
    severity = Column(Integer, default=None, nullable=True)
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

    aggregated_recommendations: Mapped[List["AggregatedRecommendation"]] = relationship(
        secondary=findings_aggregated_association_table, back_populates="findings"
    )

    def from_data(self, data: Content):
        self.cve_id_list = (
            [x.model_dump() for x in data.cve_id_list] if data.cve_id_list else []
        )
        self.description_list = (
            [x.model_dump() for x in data.description_list]
            if data.description_list
            else []
        )
        self.title_list = [x.model_dump() for x in data.title_list]
        self.locations_list = (
            [x.model_dump() for x in data.location_list] if data.location_list else []
        )
        self.raw_data = data.model_dump()
        self.severity = data.severity
        self.priority = data.priority
        self.report_amount = data.report_amount
        return self

    def __repr__(self):
        return f"<Finding {self.title_list}>"


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
