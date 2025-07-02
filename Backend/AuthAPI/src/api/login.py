from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status 
from AuthAPI.src.modules.database import SessionLocal
from AuthAPI.src.models.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm    
from jose import JWTError, jwt
from AuthAPI.src.models.models import CreateUserRequest, Token
router = APIRouter(tags=["Login"],prefix="/login")
SECRET_KEY="ThisIsSecretAuthKey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth2_bearer = OAuth2PasswordBearer(tokenUrl="login/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] 

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db_dependency: db_dependency, user: CreateUserRequest):
    existing_user = db_dependency.query(Users).filter(Users.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    hashed_password = bcrypt_context.hash(user.password)
    new_user = Users(username=user.username, password=hashed_password)
    db_dependency.add(new_user)
    db_dependency.commit()
    return {"message": "User created successfully"}