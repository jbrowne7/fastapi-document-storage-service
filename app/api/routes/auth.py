from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

@router.post("/login")
def login(request: LoginRequest):
    return {"message": "Login successful"}

@router.post("/register")
def register(request: RegisterRequest):
    return {"message": "Registration successful"}