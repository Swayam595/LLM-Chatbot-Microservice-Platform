""" Database session provider module """
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

class SessionProvider:
    """Session provider."""
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        async with self._session_factory() as session:
            yield session
