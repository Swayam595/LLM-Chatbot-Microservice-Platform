"""Reset password schemas"""
from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    """Forgot password request"""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request"""

    reset_password_token: str
    new_password: str = Field(..., min_length=6)
