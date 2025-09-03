from pydantic import BaseModel
from fastapi import File, UploadFile, APIRouter, Depends
from app.api.deps import get_current_user
from app.auth.jwt import decode_token
from app.db import crud


router = APIRouter(prefix="/documents")

@router.post("/upload")
async def upload_document(current_user = Depends(get_current_user), file = UploadFile):
    return {"filename": file.filename}