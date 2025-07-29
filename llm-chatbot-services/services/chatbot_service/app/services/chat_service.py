"""Service for the chat service"""

from shared.logger import get_logger
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.conversation_client import ConversationClient
from app.llm.factory import get_llm_provider

class ChatService:
    """Service for the chat service"""

    def __init__(self):
        """Initialize the chat service"""
        self.logger = get_logger(service_name="chat_service")
        self.conversation_client = ConversationClient()
        self.llm_provider = None

    async def handle_chat(self, request: ChatRequest, provider: str) -> ChatResponse:
        """Handle the chat request"""
        self.llm_provider = get_llm_provider(provider)
        self.logger.info(f"Handling chat request for user {request.user_id}")
        history = await self.conversation_client.get_user_history(request.user_id)
        semantic_search_results = await self.conversation_client.get_semantic_search_results(request.user_id, request.message)

        prompt = self._build_prompt(history, request.message, semantic_search_results)
        response = await self.llm_provider.generate_response(prompt)
        reply = self._parse_response(response)
        await self.conversation_client.save_message(request.user_id, request.message)
        await self.conversation_client.save_message(request.user_id, reply)
        return ChatResponse(response=reply)

    def _build_prompt(self, history: list[dict], current_message: str, semantic_search_results: dict[list[str]]) -> str:
        """Build the prompt for the chat"""
        self.logger.info(f"Building prompt for user from last 20 messages. Number of available messages: {len(history)}")
        conversation_snippets = "\n".join(
            [f"{item['message']}" for item in history]  
        )

        if len(semantic_search_results["matches"]) > 0:
            conversation_snippets += "\n\nSemantic search results:\n"
            conversation_snippets += "\n".join(semantic_search_results["matches"])
        else:
            conversation_snippets += "\n\nNo semantic search results found."

        return f"Conversation so far:\n{conversation_snippets}\nUser: {current_message}"

    def _parse_response(self, response: str) -> str:
        """Parse the response from the LLM"""
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]