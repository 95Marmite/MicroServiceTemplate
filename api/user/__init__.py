from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.user import User
from database.database import SessionLocal, engine, Base
from api.user.crud import get_user, create_user, delete_user, update_password
from api.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from main import get_db

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/users", status_code=201)
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    return create_user(db, username, hashed_password)


@user_router.delete("/users/{username}")
def delete_user_endpoint(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="You can only delete your own user")
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return {"message": "User deleted successfully"}


@user_router.put("/users/{username}/password")
def change_password_endpoint(
    username: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.username != username:
        raise HTTPException(
            status_code=403, detail="You can only change your own password"
        )
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = get_password_hash(new_password)
    update_password(db, user, hashed_password)
    return {"message": "Password changed successfully"}
