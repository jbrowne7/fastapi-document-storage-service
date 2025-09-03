from pydantic import BaseModel
from fastapi import File, UploadFile, APIRouter, Depends
from app.api.deps import get_current_user
from app.auth.jwt import decode_token
from app.db import crud
# from app.services.storage import upload_fileobj
from app.core.config import settings


router = APIRouter(prefix="/documents")

@router.post("/upload")
async def upload_document(file: UploadFile, current_user = Depends(get_current_user)):
    # result = upload_file(str(file.filename), settings.S3_BUCKET, file.file)
    return {"filename": file.filename}