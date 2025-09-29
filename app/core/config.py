from __future__ import annotations
import sys
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError

class Settings(BaseSettings):
    APP_NAME: str = Field("fastapi-document-storage-service", description="Application name")
    JWT_SECRET: str = Field("changeme", min_length=1, description="JWT signing secret")
    JWT_ALG: str = Field("HS256", description="JWT algorithm, e.g. HS256")
    ACCESS_TOKEN_EXPIRES_MIN: int = Field(60, gt=0, description="Access token TTL (minutes)")
    AWS_ACCESS_KEY_ID: str = Field("test", description="AWS access key ID")
    AWS_SECRET_ACCESS_KEY: str = Field("test", description="AWS secret access key")
    S3_BUCKET: str = Field("fastapi-documents", description="S3 bucket name")
    S3_REGION: str = Field("eu-west-1", description="S3 region")
    S3_ENDPOINT_URL: str = Field("http://localhost:4566", description="S3 endpoint URL")
    S3_USE_SSL: bool = Field(False, description="Use SSL for S3")
    S3_FORCE_PATH_STYLE: bool = Field(True, description="Force path-style addressing for S3")

    DATABASE_USER: str = Field("postgres", description="Database username")
    DATABASE_PASSWORD: str = Field("postgres", description="Database password")
    DATABASE_HOST: str = Field("localhost", description="Database host")
    DATABASE_PORT: str = Field("5432", description="Database port")
    DATABASE_NAME: str = Field("fastapi_docstore", description="Database name")
    DATABASE_URL: str = "" #db url is set in constructor


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(self, **values):
        super().__init__(**values)
        self.DATABASE_URL = (
            f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

try:
    settings = Settings() # type: ignore

    # Check for and warn if using default environment variables
    defaults = Settings.model_fields
    used_defaults = []
    for field, meta in defaults.items():
        env_key = meta.validation_alias if isinstance(meta.validation_alias, str) else field
        env_val = os.getenv(env_key)
        if env_val is None and getattr(settings, field) == meta.default:
            used_defaults.append(field)
    if used_defaults:
        print(
            f"WARNING: The following settings are using default values: {', '.join(used_defaults)}.\n"
            "Please set them in your .env file for production.",
            file=sys.stderr
        )

except ValidationError as e:
    print("Configuration error: missing/invalid environment variables.", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)
