from typing import BinaryIO, Optional
from pathlib import PurePosixPath
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from app.core.config import settings

_s3 = None

def s3_client():
    global _s3
    if _s3: return _s3

    _s3_client = boto3.client('s3', region_name=settings.S3_REGION, endpoint_url=settings.S3_ENDPOINT_URL)
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

# def upload_fileobj(user_id: str, doc_id: str, filename: str, fileobj: BinaryIO) -> dict:
#     s3 = s3_client()
#     try:
#         response = s3.upload_fileobj(fileobj, settings.S3_BUCKET, object_name)
#     except ClientError as e:
#         return False
#     return True