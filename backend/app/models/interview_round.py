from sqlalchemy import Column, Integer, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.base import Base


class RoundType(str, enum.Enum):
    OA = "OA"
    PHONE_SCREEN = "PHONE_SCREEN"
    TECHNICAL = "TECHNICAL"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"
    HR = "HR"
    ONSITE = "ONSITE"


class RoundStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    PASSED = "PASSED"
    FAILED = "FAILED"
    PENDING = "PENDING"


class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    round_number = Column(Integer, nullable=False)
    round_type = Column(Enum(RoundType), nullable=False)
    scheduled_date = Column(Date, nullable=True)
    status = Column(Enum(RoundStatus), nullable=False, default=RoundStatus.PENDING)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="rounds")