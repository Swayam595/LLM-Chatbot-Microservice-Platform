"""Schemas for the auth service"""

from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    """Schema for creating a user"""

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["admin", "user"] = "user"
