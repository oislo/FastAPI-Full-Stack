import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_password_hash, get_current_user, verify_password


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/change-password", response_class=HTMLResponse)
async def change(request: Request):
    user  = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("change-password.html",  {"request": request, "user": user})



@router.post("/change-password", response_class=HTMLResponse)
async def change_password(request: Request, username: str = Form(...), oldpassword: str = Form(...),
                newpassword: str = Form(...), db: Session = Depends(get_db)):
    user  = await get_current_user(request)
    if not user:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)


    msg = "Invalid name or password"

    user_model = db.query(models.Users).filter(models.Users.username == username).first()
    if user_model is not None:

        if username == user_model.username and verify_password(oldpassword, user_model.hashed_password):
            if oldpassword == newpassword:
                msg = "Please enter a different password"
                return templates.TemplateResponse("change-password.html",  {"request": request, "msg": msg})
            user_model.hashed_password = get_password_hash(newpassword)
            db.add(user_model)
            db.commit()
            msg = "Password updated"
            return templates.TemplateResponse("change-password.html",  {"request": request, "msg": msg})

