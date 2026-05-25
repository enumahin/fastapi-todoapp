from typing import Annotated

from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session

from core.auth import user_dependency, admin_dependency
from core.auth.user import user_service
from core.auth.user.user_dto import UserRequest, ChangePasswordRequest, UserUpdate
from core.config.jwt_config import get_is_admin
from database.dbconfig import get_db

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_is_admin)], # Use this dependency method when you don't need the return value of the dependent function
)

@router.get("/{user_id}")
async def get_user(db: db_dependency, user_id : int = Path(gt=0)):
    return user_service.get_user(user_id, db)

@router.get("/profile", summary="Get the current user's profile")
async def get_user(user: user_dependency, db: db_dependency):
    return user_service.get_user(user.get('id'), db)

@router.put("/", summary="Update current user's profile")
async def update_user(update_request: UserUpdate, user: user_dependency, db: db_dependency):
    return user_service.update_user(user.get('id'), update_request, db)

@router.get("/change_password")
async def get_user(user: user_dependency, db: db_dependency, change_password_request: ChangePasswordRequest):
    return user_service.change_password(user.get('username'), change_password_request, db)

def add_user(user_request: UserRequest, db):
    return user_service.add_user(user_request, db)
