"""
    We use pydantic models that does the part of data
    validation.

    It is because of this we can ensure that whatever
    data is sent by the frontend is in compliance
    with the backend.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class RoleCreate(BaseModel):
    role_name: str


class Role(RoleCreate):
    role_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    user_name: str
    role_id: int
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
