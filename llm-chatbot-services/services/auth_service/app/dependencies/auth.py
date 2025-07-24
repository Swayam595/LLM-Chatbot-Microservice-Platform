"""Module for the auth dependencies"""

from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import AppConfig
from shared import get_logger
from app.schemas import TokenData, ValidatedToken
from app.dependencies.dependency_factory import (
    get_app_config,
    get_refresh_token_repository,
    get_user_repository,
)
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository

logger = get_logger(service_name="auth_service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    app_config: AppConfig = Depends(get_app_config),
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
) -> TokenData:
    """Get the current user"""
    logger.info("Getting current user by validating access token")
    return await _verify_token(
        token,
        required_token_type="access",
        app_config=app_config,
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


async def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    app_config: AppConfig = Depends(get_app_config),
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
) -> ValidatedToken:
    """Get the refreshed tokens"""
    logger.info("Validating refresh token")
    await refresh_token_repository.assert_valid_token_in_db(token)
    token_data = await _verify_token(
        token,
        required_token_type="refresh",
        app_config=app_config,
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )
    return ValidatedToken(token=token, email=token_data.email, role=token_data.role,)


async def _verify_token(
    token: str,
    required_token_type: str,
    app_config: AppConfig,
    user_repository: UserRepository,
    refresh_token_repository: RefreshTokenRepository,
) -> TokenData:
    """Verify the token"""
    try:
        payload = jwt.decode(
            token, app_config.SECRET_KEY, algorithms=[app_config.ALGORITHM]
        )

        _assert_token_payload_has_required_fields(payload)
        _assert_token_payload_is_required_token_type(payload, required_token_type)
        await _assert_token_payload_is_not_expired(
            payload, required_token_type, token, refresh_token_repository
        )

        email = payload.get("sub")
        role = payload.get("role")

        await _assert_valid_user_exists(email, user_repository)

        logger.info(f"{required_token_type} token verified successfully")
        return TokenData(email=email, role=role)

    except JWTError as e:
        logger.error(f"JWT decoding failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate {required_token_type} token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def _assert_token_payload_has_required_fields(payload: dict) -> bool:
    """Assert the token payload is valid"""
    if not _are_required_token_payload_fields_present(payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _assert_token_payload_is_required_token_type(
    payload: dict, required_token_type: str
) -> bool:
    """Assert the token payload is the required token type"""
    if not _is_token_type_is_required_token_type(payload, required_token_type):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def _assert_token_payload_is_not_expired(
    payload: dict,
    required_token_type: str,
    token: str,
    refresh_token_repository: RefreshTokenRepository,
) -> bool:
    """Assert the token payload is not expired"""
    if _is_token_expired(payload):
        await _invalidate_expired_token(
            required_token_type, token, refresh_token_repository
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def _assert_valid_user_exists(
    email: str, user_repository: UserRepository
) -> bool:
    """Assert the user exists"""
    if not await _is_user_present(email, user_repository):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token provided.User {email} not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _are_required_token_payload_fields_present(payload: dict) -> bool:
    """Assert the token payload has required fields"""
    email = payload.get("sub")
    role = payload.get("role")
    return email is not None and role is not None


def _is_token_type_is_required_token_type(
    payload: dict, required_token_type: str
) -> bool:
    """Check if the token type is the required token type"""
    token_type = payload.get("type")
    return token_type == required_token_type


def _is_token_expired(payload: dict) -> bool:
    """Check if the token is expired"""
    exp = payload.get("exp")
    expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)
    return expiration_time < datetime.now(timezone.utc)


async def _is_user_present(email: str, user_repository: UserRepository) -> bool:
    """Check if the user is present"""
    user = await user_repository.get_user_by_email(email)
    return user is not None


async def _invalidate_expired_token(
    required_token_type: str,
    token: str,
    refresh_token_repository: RefreshTokenRepository,
) -> bool:
    """Invalidate the expired token"""
    if required_token_type == "refresh":
        await refresh_token_repository.invalidate(token)
