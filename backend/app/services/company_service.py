from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.company import Company, CompanyStatus
from app.schemas.company import CompanyCreate, CompanyUpdate


def create_company(db: Session, payload: CompanyCreate) -> Company:
    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company(db: Session, company_id: int) -> Company | None:
    stmt = select(Company).where(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    )
    return db.execute(stmt).scalar_one_or_none()


def list_companies(db: Session) -> list[Company]:
    stmt = select(Company).where(Company.deleted_at.is_(None)).order_by(Company.applied_date.desc())
    return db.execute(stmt).scalars().all()


def update_company(db: Session, company_id: int, payload: CompanyUpdate) -> Company | None:
    company = get_company(db, company_id)
    if company is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


def soft_delete_company(db: Session, company_id: int) -> Company | None:
    company = get_company(db, company_id)
    if company is None:
        return None

    company.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(company)
    return company