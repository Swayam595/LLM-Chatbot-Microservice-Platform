"""Service for user-related business logic"""
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate
from app.models import User
from app.services.password import PasswordService

class UserService:
    """Service for user-related business logic"""
    def __init__(self, user_repository: UserRepository):
        """Initialize the user service"""
        self.user_repository = user_repository
        self.password_service = PasswordService()

    async def register_user(self, user: UserCreate):
        """Register a new user"""
        if await self.user_repository.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pw = self.password_service.hash_password(user.password)
        user_data = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pw
        )

        await self.user_repository.add_user(user_data)

        return {"message": "User registered successfully"}