"""Database configuration module"""
import os

class DatabaseConfig:
    """Database configuration class"""
    def __init__(self):
        """Initialize the database configuration"""
        self.database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./auth.db")
