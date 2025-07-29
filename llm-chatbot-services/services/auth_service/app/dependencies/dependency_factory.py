"""Factory for dependencies"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared import Database
from config import AppConfig
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.user_service import UserService
from app.services.reset_password_service import ResetPasswordService

_auth_service_app_config = AppConfig()


def get_app_config() -> AppConfig:
    """Get the app config"""
    return _auth_service_app_config

async def get_db_session() -> AsyncSession:
    """Get the database session"""
    db_object = Database()
    return await db_object.get_session()


def get_user_repository(db: AsyncSession = Depends(get_db_session),) -> UserRepository:
    """Get the user repository"""
    return UserRepository(db)


def get_refresh_token_repository(
    db: AsyncSession = Depends(get_db_session),
) -> RefreshTokenRepository:
    """Get the refresh token repository"""
    return RefreshTokenRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
) -> UserService:
    """Get the user service"""
    return UserService(user_repo, _auth_service_app_config, refresh_token_repo)


def get_reset_password_service(
    app_config: AppConfig = Depends(get_app_config),
    user_repo: UserRepository = Depends(get_user_repository),
) -> ResetPasswordService:
    """Get the reset password service"""
    return ResetPasswordService(app_config, user_repo)
