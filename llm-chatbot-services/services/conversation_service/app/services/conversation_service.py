""" Conversation Service """
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationCreate, ConversationRead
from app.models.conversation import Conversation
from app.services.redis import get_redis_client
import json
from config import AppConfig


class ConversationService:
    """Conversation Service"""

    def __init__(self, repo: ConversationRepository, app_config: AppConfig):
        """Initialize the service"""
        self.conversation_repo = repo
        self.redis_client = get_redis_client(app_config)
        self.redis_cache_size = app_config.REDIS_CACHE_SIZE

    async def create_conversation(self, conversation: ConversationCreate):
        """Create a new conversation"""
        saved_message = await self.conversation_repo.create_conversation(conversation)
        pydantic_obj = ConversationRead.model_validate(saved_message)

        redis_key = self.__get_cache_key(conversation.user_id)

        await self.redis_client.lpush(redis_key, pydantic_obj.model_dump_json())
        await self.redis_client.ltrim(redis_key, 0, self.redis_cache_size - 1)

        return pydantic_obj

    async def get_user_conversations(self, user_id: int, limit: int = 20):
        """Get conversations by user"""
        redis_key = self.__get_cache_key(user_id)
        limit = min(limit, self.redis_cache_size)

        cached = await self.redis_client.lrange(redis_key, 0, limit - 1)

        if cached:
            return [ConversationRead(**json.loads(msg)) for msg in cached]

        conversations = await self.conversation_repo.get_conversations_by_user(
            user_id, limit=limit
        )
        await self.__create_new_cache(user_id, conversations)
        return conversations

    async def __create_new_cache(self, user_id: int, conversations: list[Conversation]):
        """Prime the cache with the new conversations"""
        redis_key = self.__get_cache_key(user_id)
        await self.redis_client.delete(redis_key)
        for convo in conversations:
            pydantic_obj = ConversationRead.model_validate(convo)
            await self.redis_client.rpush(redis_key, pydantic_obj.model_dump_json())

    def __get_cache_key(self, user_id: int):
        """Get the cache key"""
        return f"user:{user_id}:messages"
