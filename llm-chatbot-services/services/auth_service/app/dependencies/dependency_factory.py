"""Factory for dependencies"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import AppConfig
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.user_service import UserService
from app.services.database import get_db

_auth_service_app_config = AppConfig()


def get_user_repository(db: AsyncSession = Depends(get_db),) -> UserRepository:
    """Get the user repository"""
    return UserRepository(db)


def get_refresh_token_repository(
    db: AsyncSession = Depends(get_db),
) -> RefreshTokenRepository:
    """Get the refresh token repository"""
    return RefreshTokenRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
) -> UserService:
    """Get the user service"""
    return UserService(user_repo, _auth_service_app_config, refresh_token_repo)


def get_app_config() -> AppConfig:
    """Get the app config"""
    return _auth_service_app_config
