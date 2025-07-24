"""Repository for refresh token data access"""
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
        self.logger.info("Saving new refresh token")
        new_token = RefreshTokens(token=token, user_id=user_id)
        self.db.add(new_token)
        await self.db.commit()

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
