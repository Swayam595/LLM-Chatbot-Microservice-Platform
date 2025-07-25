"""Repository for user data access"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User


class UserRepository:
    """Repository for user data access"""

    def __init__(self, db: AsyncSession):
        """Initialize the user repository"""
        # Simulate a user database
        self.__db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email"""
        user = await self.__db.execute(select(User).where(User.email == email))
        return user.scalars().first()

    async def add_user(self, user: User) -> None:
        """Add a user to the database"""
        self.__db.add(user)
        await self.__db.commit()
        await self.__db.refresh(user)

    async def update_user(self, user: User) -> None:
        """Update a user's role"""
        await self.__db.commit()
        await self.__db.refresh(user)

    async def update_user_password(self, user: User, new_hashed_password: str) -> None:
        """Update a user's password"""
        user.hashed_password = new_hashed_password
        await self.update_user(user)
