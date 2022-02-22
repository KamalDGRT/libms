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
    role_id = Column(
        Integer,
        ForeignKey("role.role_id", ondelete="CASCADE"),
        nullable=False
    )
    user_role = relationship("Role", foreign_keys=[role_id])


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
    user_profile = relationship("UserProfile", foreign_keys=[user_profile_id])


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

    book_category = relationship(
        "BookCategory", foreign_keys=[book_category_id])


class BookTransaction(Base):
    __tablename__ = "book_transaction"

    book_transaction_id = Column(Integer, primary_key=True, index=True)
    borrowed_by = Column(
        Integer,
        ForeignKey("user_profile.user_profile_id", ondelete="CASCADE"),
        nullable=False
    )
    issued_date = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    due_date = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW() + INTERVAL '5 day'")
    )
    book_fine = Column(Float, nullable=True)
    remarks = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    borrower = relationship("UserProfile", foreign_keys=[borrowed_by])


class BookBorrow(Base):
    __tablename__ = "book_borrow"

    book_borrow_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        nullable=False
    )
    book_transaction_id = Column(
        Integer,
        ForeignKey("book_transaction.book_transaction_id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(TIMESTAMP(
        timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    book_borrowed = relationship("Book", foreign_keys=[book_id])
    book_borrow_transaction = relationship(
        "BookTransaction", foreign_keys=[book_transaction_id])


class Rating(Base):
    __tablename__ = "rating"

    rating_id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        nullable=False
    )

    point = Column(Integer, nullable=False)

    given_by = Column(
        Integer,
        ForeignKey("user_profile.user_profile_id", ondelete="CASCADE"),
        nullable=False
    )

    given_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    rater = relationship("UserProfile", foreign_keys=[given_by])
    book = relationship("Book", foreign_keys=[book_id])


class Review(Base):
    __tablename__ = "review"

    review_id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("book.book_id", ondelete="CASCADE"),
        nullable=False
    )

    description = Column(String, nullable=False)

    given_by = Column(
        Integer,
        ForeignKey("user_profile.user_profile_id", ondelete="CASCADE"),
        nullable=False
    )

    given_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    reviewer = relationship("UserProfile", foreign_keys=[given_by])
    book = relationship("Book", foreign_keys=[book_id])


class StatusCode(Base):
    __tablename__ = "status_code"

    status_id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
