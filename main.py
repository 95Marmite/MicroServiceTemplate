from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)
from api.config import config
from api.view.user_view import user_router, create_user_endpoint
from api.utils.database import engine, Base, get_db

app = FastAPI(debug=True)
app.include_router(user_router)

class Token(BaseModel):
    access_token: str
    token_type: str


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.post("/token", response_model=Token)
def login_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    #create_user_endpoint("root", "root")
    uvicorn.run(app)
