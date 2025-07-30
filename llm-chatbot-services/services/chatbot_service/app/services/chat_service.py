"""Service for the chat service"""

from shared.logger import get_logger
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.conversation_client import ConversationClient
from app.llm.factory import get_llm_provider
from app.utils.errors import ServiceError


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
        history = await self._get_user_history(request.user_id)
        semantic_search_results = await self._get_semantic_search_results(
            request.user_id, request.message
        )

        prompt = self._build_prompt(history, request.message, semantic_search_results)

        response = await self._get_llm_response(prompt)
        reply = self._parse_response(response)
        await self._save_message(request.user_id, request.message)
        await self._save_message(request.user_id, reply)
        return ChatResponse(response=reply)

    async def _get_user_history(self, user_id: str) -> list[dict]:
        """Get the user history"""
        try:
            return await self.conversation_client.get_user_history(user_id)
        except Exception as e:
            self.logger.error(f"Error getting user history for user {user_id}: {e}")
            raise ServiceError(
                f"Error getting user history for user {user_id}: {e}"
            ) from e

    async def _get_semantic_search_results(self, user_id: str, message: str) -> dict:
        """Get the semantic search results"""
        try:
            return await self.conversation_client.get_semantic_search_results(
                user_id, message
            )
        except Exception as e:
            self.logger.error(
                f"Error getting semantic search results for user {user_id}: {e}"
            )
            raise ServiceError(
                f"Error getting semantic search results for user {user_id}: {e}"
            ) from e

    async def _get_llm_response(self, prompt: str) -> str:
        """Get the LLM response"""
        try:
            return await self.llm_provider.generate_response(prompt)
        except Exception as e:
            self.logger.error(f"Error getting LLM response: {e}")
            raise ServiceError(f"Error getting LLM response: {e}") from e

    async def _save_message(self, user_id: str, message: str) -> None:
        """Save the message"""
        try:
            await self.conversation_client.save_message(user_id, message)
        except Exception as e:
            self.logger.error(f"Error saving message for user {user_id}: {e}")
            raise ServiceError(f"Error saving message for user {user_id}: {e}") from e

    def _build_prompt(
        self,
        history: list[dict],
        current_message: str,
        semantic_search_results: dict[list[str]],
    ) -> str:
        """Build the prompt for the chat"""
        self.logger.info(
            f"Building prompt for user from last 20 messages. Number of available messages: {len(history)}"
        )
        conversation_snippets = "\n".join([f"{item['message']}" for item in history])

        if len(semantic_search_results["matches"]) > 0:
            conversation_snippets += "\n\nSemantic search results:\n"
            conversation_snippets += "\n".join(semantic_search_results["matches"])
        else:
            conversation_snippets += "\n\nNo semantic search results found."

        return f"Conversation so far:\n{conversation_snippets}\nUser: {current_message}"

    def _parse_response(self, response: str) -> str:
        """Parse the response from the LLM"""
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
