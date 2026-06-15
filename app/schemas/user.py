from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field

from uuid import UUID
from typing import Self
import re


class UserBase(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: UUID
    name: str = Field(max_length=50, default=UserBase.username)


class UserRegister(UserBase):
    password: str
    repeat_password: str

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.password != self.repeat_password:
            raise ValueError("passwords do not match")
        return self

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 14:
            raise ValueError("Password must be at least 14 characters long")

        if len(value) > 128:
            raise ValueError("Password is too long (max 128 characters)")

        if " " in value:
            raise ValueError("Password must not contain spaces")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>?/\\|`~]", value):
            raise ValueError("Password must contain at least one special character")

        return value
    

class UserLogin(BaseModel):
    username_or_email: str
    password: str