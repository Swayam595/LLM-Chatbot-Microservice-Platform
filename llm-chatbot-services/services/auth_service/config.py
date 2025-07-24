"""Configuration module for the auth service"""

import os
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Raised when required config values are missing"""

    _ERROR_MSG = "❌ {message}"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self._ERROR_MSG.format(message=self.message))


class AppConfig:
    """Configuration class for the auth service"""

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None
    REFRESH_TOKEN_EXPIRE_MINUTES: int | None = None

    def __init__(self):
        self.__set_config()
        self.__validate_config()

    def __set_config(self):
        """Set the configuration values"""
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = self.__get_access_token_expire_minutes()
        self.REFRESH_TOKEN_EXPIRE_MINUTES = self.__get_refresh_token_expire_minutes()

    def __validate_config(self):
        """Validate the configuration values"""
        if self.SECRET_KEY is None:
            raise ConfigError(
                "SECRET_KEY is required but not set in environment variables."
            )

        if self.ALGORITHM is None:
            raise ConfigError(
                "ALGORITHM is required but not set in environment variables."
            )

        if self.ACCESS_TOKEN_EXPIRE_MINUTES is None:
            raise ConfigError(
                "ACCESS_TOKEN_EXPIRE_MINUTES is required but not set in environment variables."
            )

        if self.REFRESH_TOKEN_EXPIRE_MINUTES is None:
            raise ConfigError(
                "REFRESH_TOKEN_EXPIRE_MINUTES is required but not set in environment variables."
            )

    def __get_access_token_expire_minutes(self) -> int | None:
        """Get the access token expire minutes"""
        value = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        return int(value) if value else None

    def __get_refresh_token_expire_minutes(self) -> int | None:
        """Get the refresh token expire minutes"""
        value = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
        return int(value) if value else None
