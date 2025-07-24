"""Module for JWT utilities"""

from typing import Dict
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import AppConfig


class JWTUtils:
    """Class for JWT utilities"""

    def __init__(self, app_config: AppConfig):
        """Initialize the JWT utilities"""
        self.secret_key = app_config.SECRET_KEY
        self.algorithm = app_config.ALGORITHM
        self.access_token_expire_minutes = app_config.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_minutes = app_config.REFRESH_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: Dict) -> str:
        """Create a short-lived access token."""
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        return self._create_token(data, expires_delta, token_type="access")

    def create_refresh_token(self, data: Dict) -> str:
        """Create a long-lived refresh token."""
        expires_delta = timedelta(minutes=self.refresh_token_expire_minutes)
        return self._create_token(data, expires_delta, token_type="refresh")

    def _create_token(
        self, data: Dict, expires_delta: timedelta, token_type: str
    ) -> str:
        """Helper to create a token with a specific type and expiry."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type": token_type})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
