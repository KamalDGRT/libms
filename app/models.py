# Every model represents a table in our database.

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True, nullable=False)
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_profile_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    residential_address = Column(String, nullable=False)

    role_id = Column(
        Integer,
        ForeignKey("role.role_id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    books_allowed = Column(
        Integer,
        default=5,
        nullable=False
    )

    user_role = relationship("Role")


class UserLogin(Base):
    __tablename__ = "user_login"
    user_login_id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(
        Integer,
        ForeignKey("user_profile.user_profile_id", ondelete="CASCADE"),
        nullable=False
    )
    email_address = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    user_profile = relationship("UserProfile")


class BookCategory(Base):
    __tablename__ = "book_category"

    book_category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True, nullable=False)
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )


class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, nullable=False, unique=True)
    book_name = Column(String, nullable=False)
    book_author = Column(String, nullable=False)
    edition = Column(Integer, nullable=False)

    book_category_id = Column(
        Integer,
        ForeignKey("book_category.book_category_id", ondelete="CASCADE"),
        nullable=False
    )

    book_price = Column(Float, nullable=False)
    book_count = Column(Integer, nullable=False)
    book_description = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    book_category = relationship("BookCategory")
