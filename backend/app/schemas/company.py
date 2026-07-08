from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.models.company import CompanyStatus


class CompanyBase(BaseModel):
    name: str
    role_title: str
    applied_date: date


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    role_title: str | None = None
    applied_date: date | None = None
    status: CompanyStatus | None = None


class CompanyResponse(CompanyBase):
    id: id
    status: CompanyStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)