"""Configuration module for the API Gateway"""

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
    """Configuration class for the API Gateway"""

    AUTH_SERVICE_URL: str | None = None
    CHATBOT_SERVICE_URL: str | None = None
    CONVERSATION_SERVICE_URL: str | None = None
    
    def __init__(self):
        self.__set_config()
        self.__validate_config()

    def __set_config(self):
        """Set the config"""
        self.AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
        self.CHATBOT_SERVICE_URL = os.getenv("CHATBOT_SERVICE_URL")
        self.CONVERSATION_SERVICE_URL = os.getenv("CONVERSATION_SERVICE_URL")

    def __validate_config(self):
        """Validate the config"""
        if not self.AUTH_SERVICE_URL:
            raise ConfigError("AUTH_SERVICE_URL is not set") 
        
        if not self.CHATBOT_SERVICE_URL:
            raise ConfigError("CHATBOT_SERVICE_URL is not set")
        
        if not self.CONVERSATION_SERVICE_URL:
            raise ConfigError("CONVERSATION_SERVICE_URL is not set")
        
        