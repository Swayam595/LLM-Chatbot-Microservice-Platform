"""Module for JWT utilities"""
from typing import Dict
from datetime import datetime, timedelta
from jose import jwt
from config import AppConfig

class JWTUtils:
    """Class for JWT utilities"""
    def __init__(self, app_config: AppConfig):
        """Initialize the JWT utilities"""
        self.secret_key = app_config.SECRET_KEY
        self.algorithm = app_config.ALGORITHM
        self.expire_minutes = app_config.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: Dict) -> str:
        """Create an access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
