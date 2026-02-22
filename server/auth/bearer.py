
import jwt
from jwt.exceptions import InvalidIssuerError, InvalidAudienceError, ExpiredSignatureError, DecodeError

from server.config import AuthSetting
from server.auth.models import LoggedInUser
from fastapi import  HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request

settings = AuthSetting() 

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> LoggedInUser:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",  
                headers={"WWW-Authenticate": "Bearer"},
            )
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,  
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = credentials.credentials
        try:
            payload = await run_in_threadpool(
                jwt.decode,
                token,
                settings.secret_jwt,
                issuer=settings.issuer,
                audience=settings.audience,
                algorithms=[settings.algorithm],
                options={"require": ["exp", "iss", "aud"]},
            )
            return LoggedInUser.model_validate(payload)  
        except (InvalidIssuerError, InvalidAudienceError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (DecodeError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )