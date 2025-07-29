from fastapi import APIRouter, Depends
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, service: ChatService = Depends()):
    return await service.handle_chat(request)
