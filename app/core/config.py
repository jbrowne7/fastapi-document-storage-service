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