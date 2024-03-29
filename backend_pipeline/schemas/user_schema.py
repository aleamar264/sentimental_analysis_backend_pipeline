from enum import Enum
from pydantic import BaseModel, EmailStr, model_validator, Field, SecretStr
from typing import Self
from utils.fastapi.auth.utils import check_password


class Roles(Enum):
    ADMIN = "admin"
    USER = "user"


class AuthSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @model_validator(mode="after")
    def check_password_sha(self) -> Self:
        hashed_password = ""
        if (
            check_password(self.password.get_secret_value(), hashed_password)
            is False
        ):
            raise ValueError("Password must be hashed")
        return self


class UserSchema(BaseModel):
    email: EmailStr
    name: str
    last_name: str | None = None
    username: str


class ExtraUserInfoModel(BaseModel):
    phone: str | None = Field(default=None, max_length=14)
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: int | None = None
    country: str | None = None
    is_active: bool = True
    role: Roles = Roles.USER


class CreateUserSchema(UserSchema, ExtraUserInfoModel):
    password1: SecretStr = Field(min_length=8)
    password2: SecretStr = Field(min_length=8)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if (
            self.password1.get_secret_value()
            != self.password2.get_secret_value()
        ):
            raise ValueError("Passwords must match")
        return self


class ResponseUserSchema(UserSchema, ExtraUserInfoModel):
    id: int
