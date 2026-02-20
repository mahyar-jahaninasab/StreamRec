from typing import Dict, Optional
from starlette.concurrency import run_in_threadpool
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError, ExpiredSignatureError
import jwt
from server.config import AuthSetting

settings = AuthSetting()
                                                                                            
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
        self.auto_error_user = auto_error
    async def __call__(self,request:Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)
        if not credentials:
            if self.auto_error_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authorization code"
                )
            return None 
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid authentication scheme."
            )
        token = credentials.credentials
        try:
            payload = run_in_threadpool(
                jwt.decode,
                token, 
                settings.secret_jwt,
                issuer=settings.issuer,           
                audience=settings.audience,   
                algorithms=[settings.algorithm],
                options={"require": ["exp", "iss", "aud"]},
            )
            return payload
        
        except jwt.InvalidIssuerError:
            raise HTTPException(401, "Invalid issuer")
        except jwt.InvalidAudienceError: 
            raise HTTPException(401, "Invalid audience")
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.DecodeError:
            raise HTTPException(403, "Invalid token")
        except ExpiredSignatureError:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token expired."
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid token."
            )

