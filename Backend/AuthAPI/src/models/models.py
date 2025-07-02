from pydantic import BaseModel, EmailStr
from AuthAPI.src.modules.database import Base
from sqlalchemy import Column, Integer, String



class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<User(username={self.username})>"