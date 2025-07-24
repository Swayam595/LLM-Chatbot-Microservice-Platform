"""Module for the role dependencies"""

from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.schemas import TokenData


def require_role(required_role: str):
    """Require a role"""

    def role_dependency(current_user: TokenData = Depends(get_current_user)):
        """Role dependency"""
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {required_role}",
            )
        return current_user

    return role_dependency
