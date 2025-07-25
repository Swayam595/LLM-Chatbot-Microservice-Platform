""" Conversation Service Dependencies """
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService

def get_conversation_repo(db: AsyncSession = Depends(get_db)):
    """Get the conversation repository"""
    return ConversationRepository(db)

def get_conversation_service(conversation_repo: ConversationRepository = Depends(get_conversation_repo)):
    """Get the conversation service"""
    return ConversationService(conversation_repo)