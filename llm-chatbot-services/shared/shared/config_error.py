"""Configuration error module for the all services"""


class ConfigError(Exception):
    """Raised when required config values are missing"""

    _ERROR_MSG = "❌ {message}"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self._ERROR_MSG.format(message=self.message))
