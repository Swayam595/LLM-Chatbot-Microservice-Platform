"""Service for password-related business logic"""

from passlib.context import CryptContext


class PasswordService:
    """Service for password-related business logic"""

    def __init__(self):
        """Initialize the password service"""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)

    def verify(self, password, hashed_password):
        """Verify Password"""
        return self.pwd_context.verify(password, hashed_password)
