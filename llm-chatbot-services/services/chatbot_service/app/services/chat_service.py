"""Service for the chat service"""

from shared.logger import get_logger
from app.schemas.chat_schema import ChatRequest, ChatResponse


class ChatService:
    """Service for the chat service"""

    def __init__(self):
        """Initialize the chat service"""
        self.logger = get_logger(service_name="chat_service")

    async def handle_chat(self, request: ChatRequest) -> ChatResponse:
        """Handle the chat request"""
        self.logger.info(f"Handling chat request for user {request.user_id}")
        # TODO: Fetch history, build prompt, call LLM
        return ChatResponse(response=f"Echo: {request.message}")
