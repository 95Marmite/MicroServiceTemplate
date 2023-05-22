import logging.config
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
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

from config import api

app = FastAPI(debug=True)
logging.config.fileConfig("config/logging.conf")


# Dependency to get database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = get_db()
    user = get_user(db, "root")
    if user:
        print("User exist")
    hashed_password = get_password_hash("Test")
    return create_user(db, "root", hashed_password)


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    authenticated_user = authenticate_user(db, username, hashed_password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(
        {"sub": authenticated_user.username}, expires_delta=None
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=api.api_host,
        port=api.api_port,
    )
