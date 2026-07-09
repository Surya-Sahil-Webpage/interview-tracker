import os
from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    correct_username = os.getenv("AUTH_USERNAME")
    correct_password_hash = os.getenv("AUTH_PASSWORD_HASH")

    if payload.username != correct_username or not verify_password(payload.password, correct_password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(payload.username)
    return TokenResponse(access_token=token)