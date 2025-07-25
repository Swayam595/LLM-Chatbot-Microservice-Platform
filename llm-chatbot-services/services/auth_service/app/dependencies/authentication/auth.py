"""Module for the auth dependencies"""


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

from .assert_token_validity import (
    assert_token_payload_has_required_fields,
    assert_token_payload_is_required_token_type,
    assert_valid_user_exists,
)
from .invalidate_token import if_expired_invalidate_token

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


async def validate_forgot_password_token(
    token: str,
    app_config: AppConfig,
    user_repository: UserRepository,
    refresh_token_repository: RefreshTokenRepository,
) -> TokenData:
    """Validate the forgot password token"""
    logger.info("Validating forgot password token")
    return await _verify_token(
        token,
        required_token_type="forgot_password",
        app_config=app_config,
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


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

        assert_token_payload_has_required_fields(payload)
        assert_token_payload_is_required_token_type(payload, required_token_type)

        email = payload.get("sub")
        role = payload.get("role")

        await assert_valid_user_exists(email, user_repository)

        logger.info(f"{required_token_type} token verified successfully")
        return TokenData(email=email, role=role)
    except JWTError as e:
        logger.error(f"JWT decoding failed: {str(e)}")
        await if_expired_invalidate_token(
            token, required_token_type, refresh_token_repository, e
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate {required_token_type} token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"An error occurred: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
