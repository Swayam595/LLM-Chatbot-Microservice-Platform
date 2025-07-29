"""Chat Service Routes"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from shared import get_logger
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

logger = get_logger(service_name="chatbot_service")
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(
    request: ChatRequest,
    service: ChatService = Depends(),
    provider: str = Query(default="gemini"),
):
    """Chat endpoint"""
    logger.info("Chat endpoint called")
    try:
        return await service.handle_chat(request, provider)
    except ValueError as e:
        logger.error(f"Value Error in chat endpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
