"""Conversation Service Dependencies"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared import Database
from config import AppConfig
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService
from app.services.vector_db_service import VectorDBService


_conversation_service_app_config = AppConfig()


def get_app_config() -> AppConfig:
    """Get the app config"""
    return _conversation_service_app_config


async def get_db_session() -> AsyncSession:
    """Get the database session"""
    db_object = Database()
    return await db_object.get_session()


def get_conversation_repo(
    db: AsyncSession = Depends(get_db_session),
) -> ConversationRepository:
    """Get the conversation repository"""
    return ConversationRepository(db)


def get_conversation_service(
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
    app_config: AppConfig = Depends(get_app_config),
):
    """Get the conversation service"""
    return ConversationService(conversation_repo, app_config)


def get_vector_db_service():
    """Get the vector database service"""
    return VectorDBService()
