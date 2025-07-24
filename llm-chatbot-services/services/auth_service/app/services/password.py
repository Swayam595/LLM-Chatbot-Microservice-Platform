"""Service for password-related business logic"""

from passlib.context import CryptContext
from shared.logger import get_logger


class PasswordService:
    """Service for password-related business logic"""

    def __init__(self):
        """Initialize the password service"""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__logger = get_logger(service_name="auth_service")

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        self.__logger.debug("Hashing password")
        return self.pwd_context.hash(password)

    def verify(self, password, hashed_password):
        """Verify Password"""
        self.__logger.debug("Verifying password")
        return self.pwd_context.verify(password, hashed_password)
