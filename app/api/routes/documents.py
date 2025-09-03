from fastapi import UploadFile, APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.services.storage import upload_fileobj, list_user_objects, delete_user_object, DuplicateFilenameError, ObjectNotFoundError
from uuid import uuid4


router = APIRouter(prefix="/documents")

@router.post("/upload")
async def upload_document(file: UploadFile, current_user = Depends(get_current_user)):
    doc_id = str(uuid4())
    try:
        result = upload_fileobj(str(current_user.id), doc_id, str(file.filename), file.file)
        return result
    except DuplicateFilenameError:
        raise HTTPException(status_code=400, detail={"code": "file already exists", "filename": file.filename})

@router.get("/list")
def list_documents(current_user = Depends(get_current_user)):
    objects = list_user_objects(current_user.id)
    return objects

@router.delete("/delete/{filename}")
def delete_document(filename: str, current_user = Depends(get_current_user)):
    try:
        delete_user_object(str(current_user.id), filename)
    except ObjectNotFoundError:
        raise HTTPException(status_code=404, detail={"code": "file not found", "filename": filename})
    return