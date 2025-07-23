"""Schemas for tokens"""
from pydantic import BaseModel, EmailStr

class TokenData(BaseModel):
    """Schema for the data encoded in the JWT."""
    email: EmailStr
    role: str