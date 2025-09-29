import boto3
import os

from typing import BinaryIO, Optional
from pathlib import PurePosixPath
from botocore.exceptions import ClientError
from app.core.config import settings

class DuplicateFilenameError(Exception): ...
class ObjectNotFoundError(Exception): ...

_s3 = None

def s3_client():
    global _s3
    if _s3: return _s3

    # # If deploying in ECS use IAM role instead of keys
    # if settings.AWS_SECRET_ACCESS_KEY or settings.AWS_ACCESS_KEY_ID:
    #     _s3_client = boto3.client(
    #         's3',
    #         region_name=settings.S3_REGION,
    #         endpoint_url=settings.S3_ENDPOINT_URL,
    #         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     )
    # else:
    _s3_client = boto3.client(
        's3',
        region_name=settings.S3_REGION,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )
    _s3 = _s3_client
    
    return _s3

def ensure_bucket(bucket_name: str) -> None:
    s3 = s3_client()
    try:
        s3.head_bucket(Bucket=bucket_name)
        return
    except ClientError as e:
        pass
    
    location = {'LocationConstraint': settings.S3_REGION}
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

def _find_user_key_by_filename(user_id: str, filename: str) -> Optional[str]:
    s3 = s3_client()
    prefix = f"users/{user_id}/docs/"
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=settings.S3_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/") or PurePosixPath(key).name != filename:
                continue
            return key
    return None

def upload_fileobj(user_id: str, doc_id: str, filename: str, fileobj: BinaryIO) -> dict:
    s3 = s3_client()
    if _find_user_key_by_filename(user_id, filename):
        raise DuplicateFilenameError(filename)
    key = f"users/{user_id}/docs/{doc_id}/{filename}"
    s3.upload_fileobj(Fileobj=fileobj, Bucket=settings.S3_BUCKET, Key=key)
    return {"bucket": settings.S3_BUCKET, "key": key, "doc_id": doc_id}

def list_user_objects(user_id: str) -> list[dict]:
    s3 = s3_client()
    prefix = f"users/{user_id}/docs/"
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=settings.S3_BUCKET, Prefix=prefix)

    objects = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                path = PurePosixPath(obj['Key'])
                doc_id = path.parts[3]
                filename = path.name
                objects.append({
                    "doc_id": doc_id,
                    "filename": filename,
                    "last_modified": obj['LastModified'],
                    "size": obj['Size'],
                    "storage_class": obj['StorageClass'],
                })

    return objects

def delete_user_object(user_id: str, filename: str) -> None:
    key = _find_user_key_by_filename(user_id, filename)
    if not key:
        raise ObjectNotFoundError(filename)
    s3_client().delete_object(Bucket=settings.S3_BUCKET, Key=key)
    