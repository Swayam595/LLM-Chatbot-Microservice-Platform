from app.schemas import TokenData
from app.repositories.user_repository import UserRepository
from app.services.token_generator import TokenGenerator
from config import AppConfig


class RefreshTokenService:
    """Service for refreshing tokens"""

    def __init__(self, app_config: AppConfig, user_repository: UserRepository):
        """Initialize the refresh token service"""
        self.app_config = app_config
        self.user_repository = user_repository
        self.token_generator = TokenGenerator(app_config)

    async def get_new_tokens(self, current_user: TokenData):
        """Refresh the access token for a user"""
        user = await self.user_repository.get_user_by_email(current_user.email)
        return await self.token_generator.get_new_tokens(user)
