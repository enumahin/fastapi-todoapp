from fastapi import HTTPException
from passlib.context import CryptContext

from core import config
from core.auth.dto import AuthResponse
from core.auth.user.user_dto import UserRequest, UserResponse, UserUpdate
from core.auth.user.user_model import User, UserRole
from core.auth.user import user_dao

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_user(user_request: UserRequest, db):
    user = User()
    user.role = UserRole.USER
    user.username = user_request.username
    user.email = user_request.email
    user.first_name = user_request.first_name
    user.last_name = user_request.last_name
    user.phone_number = user_request.phone_number
    user.hashed_password = bcrypt_context.hash(user_request.password)
    user.is_active = True
    try:
        response = user_dao.add_user(user, db)
        if isinstance(response, User):
            return get_user_response_from_user(response)
        else:
            raise HTTPException(status_code=500, detail=str(response))
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Error creating user: " + str(ex))

def get_user(user_id: int, db):
    user = user_dao.get_user(user_id, db)
    if user is not None:
        return get_user_response_from_user(user)
    raise HTTPException(status_code=404, detail="User not found")


def authenticate_user(email: str, password: str, db):
    user = user_dao.get_user_by_email_or_username(email, db)
    all_users = db.query(User).all()
    if user and bcrypt_context.verify(password, user.hashed_password):
        key = user.username
        if key is None:
            key = user.email
        access_token = config.jwt_config.create_access_token(key, user.id)
        refresh_token = config.jwt_config.create_refresh_token(key, user.id)
        user_response = get_user_response_from_user(user)
        return AuthResponse(user=user_response, access_token=access_token, refresh_token=refresh_token)
    raise HTTPException(status_code=401, detail="Invalid email or password")


def change_password(username, change_password_request, db):
    user = user_dao.get_user_by_email_or_username(username, db)
    if user and bcrypt_context.verify(change_password_request.old_password, user.hashed_password):
        user.hashed_password = bcrypt_context.hash(change_password_request.new_password)
        db.commit()
        return "Password changed successfully"
    raise HTTPException(status_code=401, detail="Invalid user details")

def update_user(user_id: int, update_request: UserUpdate, db):
    user = user_dao.get_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    if update_request.first_name:
        user.first_name = update_request.first_name
    if update_request.last_name:
        user.last_name = update_request.last_name
    if update_request.phone_number:
        user.phone_number = update_request.phone_number
    db.commit()
    return get_user_response_from_user(user)

def get_user_response_from_user(user: User):
    return UserResponse(id=user.id, email=user.email, username=user.username, first_name=user.first_name,
                        last_name=user.last_name, phone_number=user.phone_number,
                        role=user.role, is_active=user.is_active)