from app.services.jwt_utils import JWTUtils
from app.models import User
from config import AppConfig
from shared.logger import get_logger


class TokenGenerator:
    """Service for generating tokens"""

    def __init__(self, app_config: AppConfig):
        """Initialize the token generator"""
        self.app_config = app_config
        self.jwt_utils = JWTUtils(app_config)
        self.__logger = get_logger(service_name="auth_service")

    async def get_new_tokens(self, user: User):
        """Generate new tokens for a user"""
        self.__logger.info(f"Generating new tokens for user: {user.email}")
        token_payload = {"sub": user.email, "role": user.role}
        access_token_expiry_time_in_seconds = (
            self.app_config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        refresh_token_expiry_time_in_seconds = (
            self.app_config.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )
        access_token = self.jwt_utils.create_access_token(
            data={
                **token_payload,
                "type": "access",
                "exp": access_token_expiry_time_in_seconds,
            }
        )
        refresh_token = self.jwt_utils.create_refresh_token(
            data={
                **token_payload,
                "type": "refresh",
                "exp": refresh_token_expiry_time_in_seconds,
            }
        )

        self.__logger.info(f"New Tokens generated for user: {user.email}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "access_token_expiry_time_in_seconds": access_token_expiry_time_in_seconds,
            "refresh_token_expiry_time_in_seconds": refresh_token_expiry_time_in_seconds,
        }
