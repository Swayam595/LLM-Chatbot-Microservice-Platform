"""Schemas for the auth service"""
from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    """Schema for logging in a user"""
    email: EmailStr
    password: str = Field(..., min_length=6)
