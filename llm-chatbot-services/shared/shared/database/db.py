"""Database session provider module"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from shared import Base
from .config import DatabaseConfig
from .engine import DatabaseEngine
from .session import SessionProvider

class Database:
    """Database class"""
    def __init__(self):
        """Initialize the database"""
        self._config = DatabaseConfig()
        self._engine = DatabaseEngine(self._config)
        self._session_provider = SessionProvider(self._engine.session_factory)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session for FastAPI Depends"""
        async for session in self._session_provider.get_session():
            yield session

    async def get_session(self) -> AsyncSession:
        """Get a database session"""
        generator = self.get_db()
        return await generator.__anext__()


    async def init_db(self):
        """Create all tables."""
        async with self._engine.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def shutdown_db(self):
        """Shutdown the database."""
        await self._engine.engine.dispose()
