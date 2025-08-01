"""Configuration module for the chat service"""

import os
from dotenv import load_dotenv
from shared import BaseAppConfig, ConfigError

load_dotenv()


class AppConfig(BaseAppConfig):
    """Configuration class for the chat service"""

    CONVERSATION_SERVICE_URL: str | None = None
    GEMINI_API_KEY: str | None = None
    GEMINI_URL: str | None = None

    def __init__(self):
        self.set_config()
        self.validate_config()

    def set_config(self):
        """Set the configuration values"""
        self.CONVERSATION_SERVICE_URL = os.getenv("CONVERSATION_SERVICE_URL")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_URL = os.getenv("GEMINI_URL")

    def validate_config(self):
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
