from typing import List
from fastapi import Depends,HTTPException,status
from .bearer import JWTBearer
from .models import Principal


async def get_current_user(principal: Principal = Depends(JWTBearer())) -> Principal: 
    return principal

def require_roles(required_roles: List[str]):
    def dependency(user: Principal = Depends(get_current_user)) -> Principal:
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {required_roles}"
            )
        return user
    return dependency

async def get_current_active_admin(user: Principal = Depends(get_current_user)) -> Principal:
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin required")
    return user


async def get_current_tenant_user(expected_tenant: str,user: Principal = Depends(get_current_user)) -> Principal:
    if user.tenant_id != expected_tenant:
        raise HTTPException(
            status_code=403, 
            detail=f"Tenant mismatch. Expected: {expected_tenant}"
        )
    return user