from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from AuthAPI.src.modules.auth_handler import AuthHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Update path if needed


class JWTBearer:
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error
        self.auth_handler = AuthHandler()

    async def __call__(self, request: Request) -> dict:
        # Extract token from Authorization header
        token: str = await oauth2_scheme(request)
        if not token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authorization token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate token and extract payload
        payload = self.auth_handler.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload  # You can use this in routes for accessing user_id, etc.
