"""Database engine module"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.services.database.config import DatabaseConfig

class DatabaseEngine:
    """Database engine class"""
    def __init__(self, config: DatabaseConfig):
        """Initialize the database engine"""
        self.engine = create_async_engine(config.database_url, echo=True, future=True)
        self.session_factory = sessionmaker( # type: ignore
            bind = self.engine, # type: ignore
            class_ = AsyncSession,
            expire_on_commit = False,
        )