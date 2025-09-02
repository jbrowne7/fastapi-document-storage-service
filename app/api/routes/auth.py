from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from app.db import crud
from app.db.base import get_db
from passlib.context import CryptContext
import os, datetime as dt
import jwt

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("JWT_SECRET", "x")
ALGORITHM = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", 60))

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

    return {"access_token": token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRES_MIN}

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db, request.email, request.full_name, hash_password(request.password))
    return {"message": "Registration successful", "email": user.email, "full_name": user.full_name}

@router.get("/me")
def me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud.get_user_by_id(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": user.email, "full_name": user.full_name}

# Helper functions

def hash_password(password: str) -> str:
    return _pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd.verify(plain_password, hashed_password)

def create_access_token(sub: str):
    now = dt.datetime.now(dt.UTC)
    exp = now + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRES_MIN)
    payload = {"sub": sub, "iat": now, "exp": exp}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])