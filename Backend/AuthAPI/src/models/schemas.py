from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# -------------------------------
# 📥 Request Models (Input)
# -------------------------------




class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserRegister(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: UserRole



class UserLogin(BaseModel):
    username: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


# -------------------------------
# 📤 Response Models (Output)
# -------------------------------

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    message: str
    user_id: Optional[str] = None


# -------------------------------
# 🧠 Internal Models (Advanced/Future)
# -------------------------------

class UserInDB(BaseModel):
    user_id: str
    name:str
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None


class UserProfile(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    created_at: datetime
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterResponse(BaseModel):
    message: str
    user_id: str

class MeResponse(BaseModel):
    username: str
    user_id: str
    role: str  

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"