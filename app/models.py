# Every model represents a table in our database.

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String
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
    # This is gonna create another property for us for our employee table
    # so that when we retrieve our employee details, it will fetch the
    # properties of the employee_type table
    user_role = relationship("Role")
