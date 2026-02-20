from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


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


