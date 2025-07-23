"""Service for user-related business logic"""
from config import AppConfig
from fastapi import HTTPException
from app.services.jwt_utils import JWTUtils
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserLogin, TokenData
from app.models import User
from app.services.password import PasswordService

class UserService:
    """Service for user-related business logic"""
    def __init__(self, user_repository: UserRepository, app_config: AppConfig):
        """Initialize the user service"""
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.app_config = app_config
        self.jwt_utils = JWTUtils(app_config)

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

        return {"message": "User registered successfully"}

    async def login_user(self, credentials: UserLogin):
        """Login's an User"""
        user = await self.user_repository.get_user_by_email(credentials.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.password_service.verify(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
       
        return await self.__generate_tokens(user)

    async def refresh_access_token(self, current_user: TokenData):
        """Refresh the access token for a user"""
        user = await self.user_repository.get_user_by_email(current_user.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return await self.__generate_tokens(user)   

    async def __generate_tokens(self, user: User):
        """Generate tokens for a user"""
        token_payload = {"sub": user.email, "role": user.role}
        access_token = self.jwt_utils.create_access_token(data=token_payload)
        refresh_token = self.jwt_utils.create_refresh_token(data=token_payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "access_token_expiry_time_in_seconds": self.app_config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_token_expiry_time_in_seconds": self.app_config.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        }