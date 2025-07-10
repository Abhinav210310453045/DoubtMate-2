from fastapi import APIRouter, HTTPException, status, Depends
from AuthAPI.src.models.schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RegisterResponse,
    MeResponse,
    AccessTokenResponse
)
from AuthAPI.src.modules.user_service import UserService
from AuthAPI.src.modules.auth_handler import AuthHandler
from shared.src.utils.helper.jwt_bearer import JWTBearer

router = APIRouter(prefix="/auth", tags=["Authentication"])
from AuthAPI.src.constants.constants import USER_DATA_TABLE as TABLE_NAME
user_service = UserService(table_name=TABLE_NAME)
auth_handler = AuthHandler()


# ✅ PUBLIC: Register new user
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    try:
        result = await user_service.register_user(user)
        if "error" in result:
            raise HTTPException(status_code=409, detail=result["error"])
        return RegisterResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during registration: {str(e)}")


# ✅ PUBLIC: Login & get tokens
@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    try:
        result = await user_service.authenticate_user(credentials)
        if "error" in result:
            raise HTTPException(status_code=401, detail=result["error"])
        return TokenResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during login: {str(e)}")


# 🔐 PROTECTED: Refresh access token (valid for all roles)
@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(payload=Depends(JWTBearer())):
    try:
        new_token = auth_handler.create_access_token({
            "sub": payload["sub"],
            "user_id": payload["user_id"],
            "role": payload["role"]
        })
        return AccessTokenResponse(access_token=new_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error during token refresh: {str(e)}")


# 🔐 PROTECTED: Get current user info
@router.get("/me", response_model=MeResponse)
async def get_me(payload=Depends(JWTBearer())):
    try:
        return MeResponse(
            username=payload["sub"],
            user_id=payload["user_id"],
            role=payload["role"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error fetching user info: {str(e)}")
