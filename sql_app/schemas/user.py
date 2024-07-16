from pydantic import BaseModel
from .role import Role

class UserBase(BaseModel):
    name: str
    surnames: str
    age: int
    is_active: bool | None
    email: str
    created_at: str
    updated_at: str

class UserCreate(UserBase):
    password: str
    password_confirmation: str
    #avatar: str

class User(UserBase):
    id: int
    email_verified_at: str
    avatar_url: str
    rol: list[Role] = []

    class Config:
        orm_mode = True