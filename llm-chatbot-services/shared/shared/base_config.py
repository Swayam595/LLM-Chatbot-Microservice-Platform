"""Configuration module for the all services"""

from abc import ABC, abstractmethod

class BaseAppConfig(ABC):
    """Configuration class for the all services"""

    @abstractmethod
    def set_config(self):
        """Set the configuration values"""
        pass

    @abstractmethod
    def validate_config(self):
        """Validate the configuration values"""
        pass