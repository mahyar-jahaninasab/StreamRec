from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi.concurrency import run_in_threadpool
import jwt

from server.config import AuthSetting
from server.db.database import check_user
from server.auth.models import  Principal, RefreshToken
from fastapi import Depends,HTTPException,status
import secrets


settings = AuthSetting()

def authenticate_user(user: Principal = Depends(check_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(user: Principal, expires_delta: timedelta | None = None) -> str:
    payload_dict = user.model_dump()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expiry_minutes)  
    payload_dict.update({
        "type": "access",
        "jti": secrets.token_urlsafe(32),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "iss": settings.issuer,
        "aud": settings.audience
    })
    return run_in_threadpool(
        jwt.encode, payload_dict, settings.secret_jwt, algorithm=settings.algorithm
    ).result() 

     


def create_refresh_token(data: Dict[str, Any]) -> RefreshToken:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({
        "type": "refresh",
        "jti": secrets.token_urlsafe(32),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "iss": settings.issuer,
        "aud": settings.audience
    })
    encoded_token = jwt.encode(to_encode, settings.secret_jwt, algorithm=settings.algorithm)
    payload = jwt.decode(encoded_token, settings.secret_jwt, algorithms=[settings.algorithm])
    return RefreshToken.model_validate(payload)





















