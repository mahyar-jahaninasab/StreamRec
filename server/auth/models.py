import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional


class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Principal(BaseModel):
    user_id: str = Field(..., alias="sub")
    email: Optional[str] = None 
    roles: List[str] = Field(default_factory=list)
    tenant_id: Optional[str] = None
    max_context_tokens: int = 4000 
    allowed_models: List[str] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid')

class LoggedInUser(Principal):
    model_config = ConfigDict(extra='allow')  
    type: str          
    jti: str          
    iat: datetime
    exp: datetime
    iss: str
    aud: str


class RefreshToken(BaseModel):
    model_config = ConfigDict(extra='forbid')
    sub: str                  
    type: Literal["refresh"]  
    jti: str                  
    iat: datetime
    exp: datetime
    iss: str
    aud: str
