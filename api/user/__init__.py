import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth import (
    get_current_active_user,
    get_current_user,
    get_password_hash,
)
from api.user.crud import get_user, create_user, delete_user, update_password
from database.database import get_db
from database.user import User

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/", status_code=201)
def create_user_endpoint(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    logging.debug(hashed_password)
    return create_user(db, username, hashed_password)


@user_router.delete("/{username}")
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


@user_router.put("/{username}/password")
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


@user_router.get("/me")
def get_user_endpoint(current_user: User = Depends(get_current_active_user)):
    return current_user
