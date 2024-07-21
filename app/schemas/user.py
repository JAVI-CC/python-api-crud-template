from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    computed_field,
    EmailStr,
)
from importlib import import_module
from typing import Optional
from typing_extensions import Self
from schemas.role import Role
from datetime import datetime
from dependencies.regex import pydantic_password_format
from dependencies.read_env import getenv
from dependencies.date_formatter import date_format_server_to_client


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    surnames: str = Field(min_length=3, max_length=50)
    age: int = Field(min=18, max=150)
    is_active: bool | None = Field(default=True)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(pattern=pydantic_password_format)
    password_confirmation: str = Field(pattern=pydantic_password_format)
    role_id: str

    @field_validator("role_id")
    @classmethod
    def role_id_exists(cls, id: str):
        validator = import_module("schemas.validators.user_role_id")
        return validator.role_id_exists(id)

    @field_validator("email")
    @classmethod
    def email_exists(cls, email: EmailStr):
        validator = import_module("schemas.validators.user_email")
        return validator.user_email_exists(email)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        validator = import_module("schemas.validators.user_password_confirmation")
        return validator.is_match_password(
            self, self.password, self.password_confirmation
        )


class UserUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=50, default=None)
    surnames: Optional[str] = Field(min_length=3, max_length=50, default=None)
    age: Optional[int] = Field(min=18, max=150, default=None)
    is_active: Optional[bool] = Field(default=None)
    role_id: Optional[str] = Field(default=None)

    @field_validator("role_id")
    @classmethod
    def role_id_exists(cls, id: str):
        validator = import_module("schemas.validators.user_role_id")
        return validator.role_id_exists(id)


class UserUpdatePassword(BaseModel):
    password: str = Field(pattern=pydantic_password_format)
    password_confirmation: str = Field(pattern=pydantic_password_format)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        validator = import_module("schemas.validators.user_password_confirmation")
        return validator.is_match_password(
            self, self.password, self.password_confirmation
        )


class UserCreateSeeder(UserBase):
    id: str
    email_verified_at: str | None
    avatar_name_file: str | None
    hashed_password: str
    role_id: str
    created_at: datetime
    updated_at: datetime

    @field_validator("email_verified_at")
    @classmethod
    def email_verified_at_format(cls, date_verified):
        validator = import_module("schemas.validators.user_email_verified_at")
        return validator.email_verified_at_format(date_verified)


class User(UserBase):
    id: str
    email_verified_at: datetime | None
    avatar_name_file: str | None
    role: Role
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def fullname(self) -> str:
        return f"{self.name} {self.surnames}"

    @computed_field
    @property
    def avatar(self) -> list | None:
        if not self.avatar_name_file:
            return None

        return [
            {
                "filename": self.avatar_name_file,
                "path": f"{getenv('APP_URL')}/avatar/{self.avatar_name_file}",
            }
        ]

    @computed_field
    @property
    def dates_formats(self) -> list:
        return [
            {
                "email_verified_at": date_format_server_to_client(
                    str(self.email_verified_at)
                ),
                "created_at": date_format_server_to_client(str(self.created_at)),
                "updated_at": date_format_server_to_client(str(self.updated_at)),
            }
        ]

    class Config:
        from_attributes = True
