from fastapi import FastAPI,status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import AuthAPI.src.models.models as models
from AuthAPI.src.modules.database import engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()
# CORS configuration
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, adjust as needed
    allow_headers=["*"],  # Allow all headers, adjust as needed
)
