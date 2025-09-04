from __future__ import annotations
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError

class Settings(BaseSettings):
    APP_NAME: str = Field(..., description="Application name")
    DATABASE_URL: str = Field(..., description="SQLAlchemy connection URL")
    JWT_SECRET: str = Field(..., min_length=1, description="JWT signing secret")
    JWT_ALG: str = Field(..., description="JWT algorithm, e.g. HS256")
    ACCESS_TOKEN_EXPIRES_MIN: int = Field(..., gt=0, description="Access token TTL (minutes)")
    AWS_ACCESS_KEY_ID: str = Field(..., description="AWS access key ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., description="AWS secret access key")
    S3_BUCKET: str = Field(..., description="S3 bucket name")
    S3_REGION: str = Field(..., description="S3 region")
    S3_ENDPOINT_URL: str = Field(..., description="S3 endpoint URL")
    S3_USE_SSL: bool = Field(..., description="Use SSL for S3")
    S3_FORCE_PATH_STYLE: bool = Field(..., description="Force path-style addressing for S3")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

try:
    settings = Settings()  # type: ignore

except ValidationError as e:
    print("Configuration error: missing/invalid environment variables.", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)