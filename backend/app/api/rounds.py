from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.interview_round import RoundCreate, RoundUpdate, RoundResponse
from app.services import round_service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/companies/{company_id}/rounds", tags=["rounds"])


@router.post("/", response_model=RoundResponse, status_code=status.HTTP_201_CREATED)
def create_round(company_id: int, payload: RoundCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    round_obj = round_service.create_round(db, company_id, payload)
    if round_obj is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return round_obj


@router.get("/", response_model=list[RoundResponse])
def list_rounds(company_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    rounds = round_service.list_rounds_for_company(db, company_id)
    if rounds is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return rounds


@router.get("/{round_id}", response_model=RoundResponse)
def get_round(company_id: int, round_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    round_obj = round_service.get_round(db, company_id, round_id)
    if round_obj is None:
        raise HTTPException(status_code=404, detail="Round not found")
    return round_obj


@router.patch("/{round_id}", response_model=RoundResponse)
def update_round(company_id: int, round_id: int, payload: RoundUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    round_obj = round_service.update_round(db, company_id, round_id, payload)
    if round_obj is None:
        raise HTTPException(status_code=404, detail="Round not found")
    return round_obj


@router.delete("/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(company_id: int, round_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    deleted = round_service.delete_round(db, company_id, round_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Round not found")