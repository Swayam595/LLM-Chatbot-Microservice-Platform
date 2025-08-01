"""Configuration module for the conversation service"""

import os
from dotenv import load_dotenv
from shared import BaseAppConfig, ConfigError

load_dotenv()


class AppConfig(BaseAppConfig):
    """Configuration class for the conversation service"""

    REDIS_URL: str | None = None
    REDIS_CACHE_SIZE: int | None = None
    REDIS_ENTRY_EXPIRY_TIME_IN_MINS: int | None = None
    CHROMA_DB_URL: str | None = None

    def __init__(self):
        self.set_config()
        self.validate_config()

    def set_config(self):
        """Set the configuration values"""
        self.REDIS_URL = os.getenv("REDIS_URL")
        self.REDIS_CACHE_SIZE = self.__get_redis_cache_size()
        self.REDIS_ENTRY_EXPIRY_TIME_IN_MINS = (
            self.__get_redis_entry_expiry_time_in_mins()
        )
        self.CHROMA_DB_URL = os.getenv("CHROMA_DB_URL")

    def validate_config(self):
        """Validate the configuration values"""
        if self.REDIS_URL is None:
            raise ConfigError(
                "REDIS_URL is required but not set in environment variables/ docker-compose."
            )

        if self.REDIS_CACHE_SIZE is None:
            raise ConfigError(
                "REDIS_CACHE_SIZE is required but not set in environment variables."
            )

        if self.REDIS_ENTRY_EXPIRY_TIME_IN_MINS is None:
            raise ConfigError(
                "REDIS_ENTRY_EXPIRY_TIME_IN_MINS is required but not set in environment variables."
            )

        if self.CHROMA_DB_URL is None:
            raise ConfigError(
                "CHROMA_DB_URL is required but not set in environment variables."
            )

    def __get_redis_cache_size(self) -> int | None:
        """Get the Redis cache size"""
        value = os.getenv("REDIS_CACHE_SIZE")
        return int(value) if value else None

    def __get_redis_entry_expiry_time_in_mins(self) -> int | None:
        """Get the Redis entry expiry time in minutes"""
        value = os.getenv("REDIS_ENTRY_EXPIRY_TIME_IN_MINS")
        return int(value) if value else None
