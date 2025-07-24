"""Module for the user model"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

UserBase = declarative_base()


class User(UserBase):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
