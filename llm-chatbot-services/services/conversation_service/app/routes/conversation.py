""" Conversation Routes """
from fastapi import APIRouter, Depends, status, Query
from shared import get_logger
from app.schemas import ConversationCreate, ConversationRead
from app.services.conversation_service import ConversationService
from app.dependencies.dependency_factory import get_conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])

logger = get_logger(service_name="conversation_service")


@router.post(
    "/message", status_code=status.HTTP_201_CREATED, response_model=ConversationRead
)
async def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service),
):
    """Create a new conversation"""
    logger.info(f"Creating conversation endpoint called")
    return await service.create_conversation(conversation)


@router.get("/history", response_model=list[ConversationRead])
async def get_conversations(
    user_id: int = Query(...),
    limit: int = Query(default=20),
    service: ConversationService = Depends(get_conversation_service),
):
    """Get all conversations for a user"""
    logger.info(f"Getting conversations endpoint called")
    return await service.get_user_conversations(user_id, limit)


@router.delete("/history", status_code=status.HTTP_202_ACCEPTED, response_model=dict)
async def delete_conversations(
    user_id: int, service: ConversationService = Depends(get_conversation_service),
):
    """Delete all conversations for a user"""
    logger.info(f"Deleting conversations endpoint called")
    await service.delete_user_conversations(user_id)
    return {"message": f"Conversations deleted for user {user_id}"}
