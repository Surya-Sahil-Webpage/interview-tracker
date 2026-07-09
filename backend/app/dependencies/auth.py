from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username