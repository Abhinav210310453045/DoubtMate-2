from fastapi import Depends, HTTPException, status
from shared.src.utils.helper.jwt_bearer import JWTBearer

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, payload=Depends(JWTBearer())):
        user_role = payload.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return payload