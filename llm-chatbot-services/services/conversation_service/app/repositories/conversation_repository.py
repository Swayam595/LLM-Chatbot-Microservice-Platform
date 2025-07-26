""" Conversation Repository """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.conversation import Conversation
from app.schemas import ConversationCreate


class ConversationRepository:
    """Conversation Repository"""

    def __init__(self, db: AsyncSession):
        """Initialize the repository"""
        self.__db = db

    async def create_conversation(self, data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        convo = Conversation(**data.model_dump())
        self.__db.add(convo)
        await self.__db.commit()
        await self.__db.refresh(convo)
        return convo

    async def get_conversations_by_user(
        self, user_id: int, limit: int
    ) -> list[Conversation]:
        """Get conversations by user"""
        result = await self.__db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.id.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def delete_conversations_by_user(self, user_id: int):
        """Delete conversations by user"""
        await self.__db.execute(
            delete(Conversation).where(Conversation.user_id == user_id)
        )
        await self.__db.commit()
