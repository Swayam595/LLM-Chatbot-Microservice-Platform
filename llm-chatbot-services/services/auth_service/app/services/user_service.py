"""Service for user-related business logic"""
from datetime import datetime, timedelta, timezone
from config import AppConfig
from fastapi import HTTPException
from app.services.jwt_utils import JWTUtils
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserLogin
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

        access_token_expire_minutes = self.app_config.ACCESS_TOKEN_EXPIRE_MINUTES
        expiry_time = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)

        token_payload = {"sub": user.email, "role": user.role, "exp": expiry_time}
        token = self.jwt_utils.create_access_token(token_payload)
        
        return {"access_token": token, "token_type": "bearer", "expiry_time_in_seconds": access_token_expire_minutes * 60}