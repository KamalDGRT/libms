"""
    We use pydantic models that does the part of data
    validation.

    It is because of this we can ensure that whatever
    data is sent by the frontend is in compliance
    with the backend.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy import Float


class RoleCreate(BaseModel):
    role_name: str


class Role(RoleCreate):
    role_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserSimple(BaseModel):
    user_profile_id: int
    user_name: str

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

    class Config:
        orm_mode = True


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


class BookCreate(BaseModel):
    isbn: str
    book_name: str
    book_author: str
    edition: int
    book_category_id: int
    book_price: float
    book_count: int
    book_description: str

    class Config:
        orm_mode = True


class Book(BookCreate):
    book_id: int
    book_category: BookCategoryCreate

    class Config:
        orm_mode = True


class BookSimple(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_category: BookCategoryCreate

    class Config:
        orm_mode = True


class BookShort(BaseModel):
    book_id: int
    book_name: str
    book_author: str

    class Config:
        orm_mode = True


class BookComplete(BookCreate):
    created_at: datetime
    book_category: BookCategory

    class Config:
        orm_mode = True

# ------------------------------------------------------------------------------


class BookBorrowCreate(BaseModel):
    book_id: int


class BookBorrowSimple(BaseModel):
    book: BookSimple
    created_at: datetime

    class Config:
        orm_mode = True


class BookTransactionCreate(BaseModel):
    borrowed_by: int
    books: List[BookBorrowCreate]


class BookTransaction(BaseModel):
    book_transaction_id: int
    issued_date: datetime
    due_date: datetime
    borrower: UserProfileTable
    books: List[BookSimple]


# ------------------------------------------------------------------------------

class RatingCreate(BaseModel):
    book_id: int
    point: int

    class Config:
        orm_mode = True


class Rating(RatingCreate):
    rating_id: int
    book: BookSimple

    class Config:
        orm_mode = True


class RatingSimple(BaseModel):
    rating_id: int
    point: int
    book: BookShort
    rater: UserSimple

    class Config:
        orm_mode = True


class RatingUpdate(RatingSimple):
    given_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RatingComplete(RatingUpdate):
    rater: UserProfileTable

    class Config:
        orm_mode = True


# -------------------------------------------------------------------------------

class ReviewCreate(BaseModel):
    book_id: int
    description: str

    class Config:
        orm_mode = True


class Review(ReviewCreate):
    review_id: int
    book: BookSimple

    class Config:
        orm_mode = True


class ReviewSimple(BaseModel):
    review_id: int
    description: str
    book: BookShort
    reviewer: UserSimple

    class Config:
        orm_mode = True


class ReviewUpdate(ReviewSimple):
    given_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReviewComplete(ReviewUpdate):
    reviewer: UserProfileTable

    class Config:
        orm_mode = True
