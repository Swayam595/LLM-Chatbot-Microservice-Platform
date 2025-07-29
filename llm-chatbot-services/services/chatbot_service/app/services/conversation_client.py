"""Conversation Client"""
import httpx
from shared import get_logger
from app.dependencies.dependency_factory import get_app_config

class ConversationClient:
    """Conversation Client"""

    def __init__(self):
        """Initialize the Conversation Client"""
        self.logger = get_logger(service_name="conversation_client")
        self.app_config = get_app_config()
        self.base_url = self.app_config.CONVERSATION_SERVICE_URL

    async def get_user_history(self, user_id: int):
        """Get the user history"""
        self.logger.info(f"Getting user history for user {user_id}")
        response = await self._make_request(
            f"/conversations/history?user_id={user_id}", "GET", {}
        )
        return response.json()
    
    async def _make_request(self, path: str, method: str, json: dict):
        """Make a request to the conversation service"""
        self.logger.info(f"Making {method} request to {path}")
        async with httpx.AsyncClient() as client:
            response = await client.request(method, f"{self.base_url}{path}", json=json)
            response.raise_for_status()
            return response
