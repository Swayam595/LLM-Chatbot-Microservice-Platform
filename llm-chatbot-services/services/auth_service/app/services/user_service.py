"""Service for user-related business logic"""
from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate
from fastapi import HTTPException

class UserService:
    """Service for user-related business logic"""
    def __init__(self, user_repository: UserRepository):
        """Initialize the user service"""
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def register_user(self, user: UserCreate):
        """Register a new user"""
        if self.user_repository.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pw = self.__hash_password(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_pw
        }

        self.user_repository.add_user(user_data)

        return {"message": "User registered successfully"} 

    def __hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)