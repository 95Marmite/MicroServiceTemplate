from sqlalchemy.orm import Session
from sqlalchemy import select
from database.user import User
from database.database import engine


def get_user(username: str):
    with engine.connect() as conn:
        stmt = select(User).where(User.username == username)
        return conn.execute(stmt).fetchone()


def create_user(db: Session, username: str, password: str):
    user = User(username=username, hashed_password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def update_password(db: Session, user: User, new_password: str):
    user.hashed_password = new_password
    db.commit()
