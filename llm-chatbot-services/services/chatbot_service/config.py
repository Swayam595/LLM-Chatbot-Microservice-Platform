"""Configuration module for the chat service"""

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
    """Configuration class for the chat service"""

    CONVERSATION_SERVICE_URL: str | None = None
    GEMINI_API_KEY: str | None = None
    GEMINI_URL: str | None = None

    def __init__(self):
        self.__set_config()
        self.__validate_config()

    def __set_config(self):
        """Set the configuration values"""
        self.CONVERSATION_SERVICE_URL = os.getenv("CONVERSATION_SERVICE_URL")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_URL = os.getenv("GEMINI_URL")

    def __validate_config(self):
        """Validate the configuration values"""
        if self.CONVERSATION_SERVICE_URL is None:
            raise ConfigError(
                "CONVERSATION_SERVICE_URL is required but not set in environment variables/ docker-compose."
            )
        
        if self.GEMINI_API_KEY is None:
            raise ConfigError(
                "GEMINI_API_KEY is required but not set in environment variables/ docker-compose."
            )
        
        if self.GEMINI_URL is None:
            raise ConfigError(
                "GEMINI_URL is required but not set in environment variables/ docker-compose."
            )
