"""Service for user-related business logic"""

from config import AppConfig
from fastapi import HTTPException
from app.services.token_generator import TokenGenerator
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas import UserCreate, UserLogin
from app.models import User
from app.services.password import PasswordService
from shared.logger import get_logger


class UserService:
    """Service for user-related business logic"""

    def __init__(
        self,
        user_repository: UserRepository,
        app_config: AppConfig,
        refresh_token_repository: RefreshTokenRepository,
    ):
        """Initialize the user service"""
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.app_config = app_config
        self.token_generator = TokenGenerator(app_config)
        self.refresh_token_repository = refresh_token_repository
        self.__logger = get_logger(service_name="auth_service")

    async def register_user(self, user: UserCreate):
        """Register a new user"""
        if await self.user_repository.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = self.password_service.hash_password(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pw,
            role=user.role,
        )

        await self.user_repository.add_user(new_user)
        self.__logger.info(f"User registered: {user.email}")
        return {"message": "User registered successfully"}

    async def login_user(self, credentials: UserLogin):
        """Login's an User"""
        user = await self.user_repository.get_user_by_email(credentials.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.password_service.verify(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        self.__logger.info(f"User found: {user.email}")
        self.__logger.info(f"Generating new tokens for user: {user.email}")
        token_payload = await self.token_generator.get_new_tokens(user)
        await self.refresh_token_repository.save(
            token_payload["refresh_token"], user.id
        )

        return token_payload
