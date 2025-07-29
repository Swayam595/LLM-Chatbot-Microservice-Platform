"""Repository for refresh token data access"""

from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models import RefreshTokens
from shared import get_logger


class RefreshTokenRepository:
    """Repository for refresh token data access"""

    def __init__(self, db: AsyncSession):
        """Initialize the refresh token repository"""
        self.logger = get_logger(service_name="auth_service")
        self.db = db

    async def save(self, token: str, user_id: int):
        """Save a new refresh token"""
        self.logger.info("Saving (or updating) refresh token")
        existing_token = await self.__get_existing_refresh_token_if_exists(user_id)

        if existing_token:
            self.__update_existing_token(existing_token, token)
        else:
            self.__create_new_token(token, user_id)

        await self.db.commit()
        self.logger.info("Refresh token saved/updated successfully")

    async def invalidate(self, token: str):
        """Invalidate a refresh token"""
        self.logger.info("Invalidating refresh token")
        result = await self.db.execute(
            select(RefreshTokens).where(RefreshTokens.token == token)
        )
        db_token = result.scalar_one_or_none()
        if db_token:
            db_token.is_valid = False
            await self.db.commit()

    async def assert_valid_token_in_db(self, token: str) -> bool:
        """Validate a refresh token"""
        self.logger.info("Validating refresh token")
        if not await self.__is_token_valid(token):
            self.logger.error("Invalid refresh token")
            self.__raise_invalid_token_exception()

    def __raise_invalid_token_exception(self):
        """Raise an invalid token exception"""
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    async def __is_token_valid(self, token: str) -> bool:
        """Check if a refresh token is valid"""
        self.logger.info("Checking if refresh token is valid")
        result = await self.db.execute(
            select(RefreshTokens).where(
                RefreshTokens.token == token, RefreshTokens.is_valid == True
            )
        )
        return result.scalar_one_or_none() is not None

    # TODO: Delete expired tokens for all users in a cron job
    async def delete_user_expired_tokens(self, user_id: int):
        """Delete 30 days old expired refresh tokens"""
        self.logger.info("Deleting expired refresh token")
        result = await self.db.execute(
            select(RefreshTokens).where(
                RefreshTokens.user_id == user_id,
                RefreshTokens.is_valid is False,
                RefreshTokens.created_at < datetime.now() - timedelta(days=30),
            )
        )
        db_token = result.scalars().all()
        if db_token:
            await self.db.delete(db_token)
            await self.db.commit()
            self.logger.info("Expired refresh token deleted successfully")

    async def __get_existing_refresh_token_if_exists(self, user_id: int) -> bool:
        """Get an existing refresh token if it exists"""
        self.logger.info("Getting refresh token if it exists")
        result = await self.db.execute(
            select(RefreshTokens).where(RefreshTokens.user_id == user_id)
        )
        return result.scalar_one_or_none()

    def __update_existing_token(self, existing_token: RefreshTokens, token: str):
        """Update an existing refresh token"""
        self.logger.info("Updating existing refresh token")
        existing_token.token = token
        existing_token.is_valid = True

    def __create_new_token(self, token: str, user_id: int):
        """Create a new refresh token"""
        self.logger.info("Creating a new refresh token")
        new_token = RefreshTokens(token=token, user_id=user_id)
        self.db.add(new_token)
