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
    user_profile_id: int
    user_name: str
    email_address: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserProfileTable(BaseModel):
    user_profile_id: int
    user_name: str
    phone_number: str
    residential_address: str
    books_allowed: int = 5
    role_id: int = 2

    class Config:
        orm_mode = True


class UserDetail(BaseModel):
    user_name: str
    phone_number: str
    residential_address: str
    books_allowed: int = 5
    role_id: int = 2
    email_address: EmailStr


class UserCreate(UserDetail):
    password: str

    class Config:
        orm_mode = True


class UserProfile(UserDetail):
    user_profile_id: int


class UserProfileCreate(BaseModel):
    user_name: str
    phone_number: str
    residential_address: str
    books_allowed: int = 5

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_profile_id: Optional[str] = None


# ------------------------------------------------------------------------------

class BookCategoryCreate(BaseModel):
    category_name: str

    class Config:
        orm_mode = True


class BookCategory(BookCategoryCreate):
    book_category_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# -------------------------------------------------------------------------------
