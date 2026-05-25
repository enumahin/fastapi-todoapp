from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean

from database.dbconfig import Base


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User(Base):

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True)
    username: str = Column(String, unique=True)
    first_name: str = Column(String)
    last_name: str = Column(String)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    role = Column(String)
    phone_number: str = Column(String)
