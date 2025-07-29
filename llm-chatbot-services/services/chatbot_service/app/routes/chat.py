"""Chat Service Routes"""

from fastapi import APIRouter, Depends
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from shared import get_logger

logger = get_logger(service_name="chatbot_service")
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, service: ChatService = Depends()):
    """Chat endpoint"""
    logger.info(f"Chat endpoint called")
    return await service.handle_chat(request)
