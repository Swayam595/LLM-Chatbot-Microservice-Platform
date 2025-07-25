"""Service for resetting passwords"""

from fastapi import HTTPException
from app.schemas import ForgotPasswordRequest, ResetPasswordRequest
from app.repositories.user_repository import UserRepository
from app.services.jwt_utils import JWTUtils
from app.services.password import PasswordService
from app.models import User
from config import AppConfig
from shared.logger import get_logger


class ResetPasswordService:
    """Service for resetting passwords"""

    def __init__(
        self, app_config: AppConfig, user_repository: UserRepository,
    ):
        """Initialize the refresh token service"""
        self.app_config = app_config
        self.user_repository = user_repository
        self.jwt_utils = JWTUtils(app_config)
        self.password_service = PasswordService()
        self.__logger = get_logger(service_name="auth_service")

    async def get_reset_password_token(
        self, forgot_password_data: ForgotPasswordRequest
    ):
        """Get a reset password token for a user"""
        self.__logger.info(
            f"Getting reset password token for user: {forgot_password_data.email}"
        )
        user = await self.user_repository.get_user_by_email(forgot_password_data.email)
        token = self.jwt_utils.create_reset_password_token(
            {"sub": user.email, "role": user.role}
        )
        return {"reset_password_token": token}

    async def reset_password(
        self, email: str, reset_password_data: ResetPasswordRequest
    ):
        """Reset the password for a user"""
        self.__logger.info(f"Resetting password for user: {email}")
        user = await self.user_repository.get_user_by_email(email)

        self._raise_if_user_not_found(user)

        hashed_password = self.password_service.hash_password(
            reset_password_data.new_password
        )
        await self.user_repository.update_user_password(user, hashed_password)
        return {"message": "Password reset successfully"}

    def _raise_if_user_not_found(self, user: User):
        """Raise an exception if the user is not found"""
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
