""" Conversation Service """
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationCreate

class ConversationService:
    """Conversation Service"""
    def __init__(self, repo: ConversationRepository):
        """Initialize the service"""
        self.conversation_repo = repo

    async def create(self, data: ConversationCreate):
        """Create a new conversation"""
        return await self.conversation_repo.create_conversation(data)

    async def get_by_user(self, user_id: int):
        """Get conversations by user"""
        return await self.conversation_repo.get_conversations_by_user(user_id)
