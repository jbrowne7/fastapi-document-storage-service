from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User

def get_user_by_email(db: Session, email: str) -> User | None:
    user = select(User).where(User.email == email)
    return db.execute(user).scalar_one_or_none()