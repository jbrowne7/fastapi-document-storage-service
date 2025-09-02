from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User

def get_user_by_email(db: Session, email: str) -> User | None:
    user = select(User).where(User.email == email)
    return db.execute(user).scalar_one_or_none()

def create_user(db: Session, email: str, full_name: str, password_hash: str) -> User:
    new_user = User(email=email, full_name=full_name, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user