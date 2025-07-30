"""Custom error classes for the chatbot service"""


class ServiceError(Exception):
    """Base class for all service errors"""

    def __init__(self, message: str, status_code: int = 503):
        """Initialize the ServiceError"""
        self.message = message
        self.status_code = status_code
        super().__init__(message)
