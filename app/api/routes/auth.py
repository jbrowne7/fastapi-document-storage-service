from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(request: LoginRequest):
    return {"message": "Login successful"}