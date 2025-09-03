import datetime as dt
import jwt

from app.core.config import settings


def create_access_token(sub: str):
    now = dt.datetime.now(dt.UTC)
    exp = now + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
    payload = {"sub": sub, "iat": now, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])