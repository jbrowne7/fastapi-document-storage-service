from pydantic import BaseModel
from fastapi import File, UploadFile, APIRouter, Depends
from app.api.deps import get_current_user
from app.auth.jwt import decode_token
from app.db import crud
from app.services.storage import upload_fileobj, list_user_objects
from app.core.config import settings
from uuid import uuid4


router = APIRouter(prefix="/documents")

@router.post("/upload")
async def upload_document(file: UploadFile, current_user = Depends(get_current_user)):
    doc_id = str(uuid4())
    result = upload_fileobj(str(current_user.id), doc_id, str(file.filename), file.file)
    return result

@router.get("/list")
def list_documents(current_user = Depends(get_current_user)):
    objects = list_user_objects(current_user.id)
    return objects