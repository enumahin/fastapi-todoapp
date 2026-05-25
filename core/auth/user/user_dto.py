from typing import Optional

from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator


class UserRequest(BaseModel):
    email: str = Field(min_length=5)
    username: str = Field(min_length=5)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    phone_number: str = Field(min_length=10)
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=2)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)
    confirm_new_password: str = Field(min_length=6)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        return self

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse:
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    role: str
    is_active: bool

    def __init__(self, id, email, username, first_name, last_name, phone_number, role, is_active=True):
        self.id = id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.role = role
        self.is_active = is_active