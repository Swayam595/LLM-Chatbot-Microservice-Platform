"""Configuration module for the API Gateway"""

import os
from dotenv import load_dotenv
from shared import BaseAppConfig, ConfigError

load_dotenv()


class AppConfig(BaseAppConfig):
    """Configuration class for the API Gateway"""

    AUTH_SERVICE_URL: str | None = None
    CHATBOT_SERVICE_URL: str | None = None
    CONVERSATION_SERVICE_URL: str | None = None
    REDIS_URL: str | None = None

    def __init__(self):
        self.set_config()
        self.validate_config()

    def set_config(self):
        """Set the config"""
        self.AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
        self.CHATBOT_SERVICE_URL = os.getenv("CHATBOT_SERVICE_URL")
        self.CONVERSATION_SERVICE_URL = os.getenv("CONVERSATION_SERVICE_URL")
        self.REDIS_URL = os.getenv("REDIS_URL")

    def validate_config(self):
        """Validate the config"""
        if not self.AUTH_SERVICE_URL:
            raise ConfigError("AUTH_SERVICE_URL is not set")

        if not self.CHATBOT_SERVICE_URL:
            raise ConfigError("CHATBOT_SERVICE_URL is not set")

        if not self.CONVERSATION_SERVICE_URL:
            raise ConfigError("CONVERSATION_SERVICE_URL is not set")

        if not self.REDIS_URL:
            raise ConfigError("REDIS_URL is not set")
