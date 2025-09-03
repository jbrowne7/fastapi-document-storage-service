from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.api.deps import get_current_user
from app.auth.jwt import create_access_token, decode_token
from app.db import crud
from app.db.base import get_db
from passlib.context import CryptContext
from app.core.config import settings


router = APIRouter(prefix="/auth")
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(sub=str(user.id))

    return {"access_token": token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRES_MIN}

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db, request.email, request.full_name, hash_password(request.password))
    return {"message": "Registration successful", "email": user.email, "full_name": user.full_name}

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return {"email": current_user.email, "full_name": current_user.full_name}

# Helper functions

def hash_password(password: str) -> str:
    return _pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd.verify(plain_password, hashed_password)