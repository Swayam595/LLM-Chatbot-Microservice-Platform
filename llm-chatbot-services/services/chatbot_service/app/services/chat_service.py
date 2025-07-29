"""Service for the chat service"""

from shared.logger import get_logger
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.conversation_client import ConversationClient


class ChatService:
    """Service for the chat service"""

    def __init__(self):
        """Initialize the chat service"""
        self.logger = get_logger(service_name="chat_service")
        self.conversation_client = ConversationClient()

    async def handle_chat(self, request: ChatRequest) -> ChatResponse:
        """Handle the chat request"""
        self.logger.info(f"Handling chat request for user {request.user_id}")
        history = await self.conversation_client.get_user_history(request.user_id)
        
        # TODO: Build prompt using OpenAI #pylint: disable=fixme
        prompt = self._build_prompt(history, request.message)
        return ChatResponse(response=prompt)

    def _build_prompt(self, history: list[dict], current_message: str) -> str:
        """Build the prompt for the chat"""
        self.logger.info("Building prompt for user from last 5 messages")
        conversation_snippets = "\n".join(
            [f"{item['message']}" for item in history[-5:]]  
        )
        return f"Conversation so far:\n{conversation_snippets}\nUser: {current_message}"