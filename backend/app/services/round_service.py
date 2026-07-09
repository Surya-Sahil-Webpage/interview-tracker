from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.models.interview_round import InterviewRound
from app.models.company import Company
from app.schemas.interview_round import RoundCreate, RoundUpdate


def _get_active_company(db: Session, company_id: int) -> Company | None:
    stmt = select(Company).where(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    )
    return db.execute(stmt).scalar_one_or_none()


def create_round(db: Session, company_id: int, payload: RoundCreate) -> InterviewRound | None:
    company = _get_active_company(db, company_id)
    if company is None:
        return None  # router turns this into 404

    round_obj = InterviewRound(company_id=company_id, **payload.model_dump())
    db.add(round_obj)
    db.commit()
    db.refresh(round_obj)
    return round_obj


def list_rounds_for_company(db: Session, company_id: int) -> list[InterviewRound] | None:
    company = _get_active_company(db, company_id)
    if company is None:
        return None

    stmt = select(InterviewRound).where(
        InterviewRound.company_id == company_id
    ).order_by(InterviewRound.round_number)
    return db.execute(stmt).scalars().all()


def get_round(db: Session, company_id: int, round_id: int) -> InterviewRound | None:
    company = _get_active_company(db, company_id)
    if company is None:
        return None

    stmt = select(InterviewRound).where(
        InterviewRound.id == round_id,
        InterviewRound.company_id == company_id
    )
    return db.execute(stmt).scalar_one_or_none()


def update_round(db: Session, company_id: int, round_id: int, payload: RoundUpdate) -> InterviewRound | None:
    round_obj = get_round(db, company_id, round_id)
    if round_obj is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(round_obj, field, value)

    db.commit()
    db.refresh(round_obj)
    return round_obj


def delete_round(db: Session, company_id: int, round_id: int) -> bool:
    round_obj = get_round(db, company_id, round_id)
    if round_obj is None:
        return False

    db.delete(round_obj)
    db.commit()
    return True