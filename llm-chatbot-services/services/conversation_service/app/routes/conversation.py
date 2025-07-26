""" Conversation Routes """
from fastapi import APIRouter, Depends
from shared import get_logger
from app.schemas import ConversationCreate, ConversationRead
from app.services.conversation_service import ConversationService
from app.dependencies.dependency_factory import get_conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])

logger = get_logger(service_name="conversation_service")

@router.post("/message", response_model=ConversationRead)
async def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service)
):
    """Create a new conversation"""
    logger.info(f"Creating conversation for user {conversation.user_id}")
    return await service.create_conversation(conversation)

@router.get("/history", response_model=list[ConversationRead])
async def get_conversations(user_id: int, limit: int = 20, service: ConversationService = Depends(get_conversation_service)):
    """Get all conversations for a user"""
    logger.info(f"Getting conversations for user {user_id}")
    return await service.get_user_conversations(user_id, limit)
