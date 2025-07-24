from app.schemas import TokenData
from app.repositories.user_repository import UserRepository
from app.services.token_generator import TokenGenerator
from config import AppConfig
from shared.logger import get_logger


class RefreshTokenService:
    """Service for refreshing tokens"""

    def __init__(self, app_config: AppConfig, user_repository: UserRepository):
        """Initialize the refresh token service"""
        self.app_config = app_config
        self.user_repository = user_repository
        self.token_generator = TokenGenerator(app_config)
        self.__logger = get_logger(service_name="auth_service")

    async def get_new_tokens(self, current_user: TokenData):
        """Refresh the access token for a user"""
        self.__logger.info(f"Refreshing tokens for user: {current_user.email}")
        user = await self.user_repository.get_user_by_email(current_user.email)
        return await self.token_generator.get_new_tokens(user)
