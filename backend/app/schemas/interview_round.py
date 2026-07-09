from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.models.interview_round import RoundType, RoundStatus


class RoundBase(BaseModel):
    round_number: int
    round_type: RoundType
    scheduled_date: date | None = None


class RoundCreate(RoundBase):
    pass


class RoundUpdate(BaseModel):
    round_number: int | None = None
    round_type: RoundType | None = None
    scheduled_date: date | None = None
    status: RoundStatus | None = None


class RoundResponse(RoundBase):
    id: int
    company_id: int
    status: RoundStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)