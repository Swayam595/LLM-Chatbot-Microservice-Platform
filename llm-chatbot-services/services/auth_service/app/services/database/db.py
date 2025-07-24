"""Database session provider module"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.database.config import DatabaseConfig
from app.services.database import DatabaseEngine
from app.services.database import SessionProvider
from app.models.base import Base

_config = DatabaseConfig()
_engine = DatabaseEngine(_config)
_session_provider = SessionProvider(_engine.session_factory)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    async for session in _session_provider.get_session():
        yield session


async def init_db():
    """Create all tables."""
    async with _engine.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown_db():
    """Shutdown the database."""
    await _engine.engine.dispose()
