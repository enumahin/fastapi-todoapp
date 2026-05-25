import os
from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from core.auth.user import user_model
from core.auth.user.user_model import UserRole
from database.dbconfig import get_db

db_dependency = Annotated[Session, Depends(get_db)]

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret-key')
JWT_EXPIRATION_TIME = int(os.getenv('JWT_EXPIRATION_TIME', 3600))
JWT_REFRESH_EXPIRATION_TIME = int(os.getenv('JWT_REFRESH_EXPIRATION_TIME', 86400))
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(username: str, user_id: int):
    return __create_token(username, user_id, JWT_EXPIRATION_TIME)

def create_refresh_token(username: str, user_id: int):
    return __create_token(username, user_id, JWT_REFRESH_EXPIRATION_TIME)

def __create_token(username: str, user_id: int, exp: int):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + timedelta(seconds=exp)
    encode.update({'exp': expires})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

def is_token_expired(token: str):
    try:
        payload = decode_token(token)
        return payload['exp'] < datetime.now(timezone.utc)
    except jwt.ExpiredSignatureError:
        return True
    except jwt.JWTError:
        return True

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = decode_token(token)
        username = payload.get('sub')
        user_id = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if isinstance(user_id, str):
            user_id = int(user_id)
        user = db.get(user_model.User, user_id)
        if not user or (user.username != username and user.email != username):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {'username': username, 'id': user_id, 'role': user.role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError as je:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token: " + je.args[0])

async def get_is_admin(user: Annotated[user_model.User, Depends(get_current_user)]):
    if user.get('role') != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return True
