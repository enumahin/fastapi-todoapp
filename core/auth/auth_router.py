from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

from core.auth.user import user_service
from core.auth.user.user_dto import  UserRequest
from database.dbconfig import get_db

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest, db: db_dependency):
    return user_service.add_user(user_request, db)


@router.post("/login")
async def login_user(login_request: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return user_service.authenticate_user(login_request.username, login_request.password, db)


@router.post("/logout")
async def logout_user():
    return {"logged_in": False}