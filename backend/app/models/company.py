from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.base import Base


class CompanyStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    IN_PROGRESS = "IN_PROGRESS"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    GHOSTED = "GHOSTED"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    role_title = Column(String, nullable=False)
    applied_date = Column(Date, nullable=False)
    status = Column(Enum(CompanyStatus), nullable=False, default=CompanyStatus.APPLIED)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    rounds = relationship(
        "InterviewRound",
        back_populates="company",
        cascade="all, delete-orphan",
        order_by="InterviewRound.round_number",
    )

