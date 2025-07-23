"""Module for the auth dependencies"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import AppConfig
from app.schemas import TokenData
from shared import get_logger

logger = get_logger(service_name="auth_service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str, required_token_type: str) -> TokenData:
    """Verify the token"""
    app_config = AppConfig()
    try:
        payload = jwt.decode(
            token,
            app_config.SECRET_KEY,
            algorithms=[app_config.ALGORITHM]
        )
        email = payload.get("sub")
        role = payload.get("role")  
        token_type = payload.get("type")

        if email is None or role is None or token_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if required_token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(email=email, role=role)

    except JWTError as e:
        logger.error(f"JWT decoding failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate {required_token_type} token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    """Get the current user"""
    return verify_token(token, required_token_type="access")

async def validate_refresh_tokens(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    """Get the refreshed tokens"""
    return verify_token(token, required_token_type="refresh")