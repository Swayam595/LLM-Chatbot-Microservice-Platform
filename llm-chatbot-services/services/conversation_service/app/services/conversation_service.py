"""Conversation Service"""

import json
from shared import get_logger
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationCreate, ConversationRead
from app.models.conversation import Conversation
from app.services.redis import get_redis_client
from app.services.vector_db_service import VectorDBService
from config import AppConfig


class ConversationService:
    """Conversation Service"""

    def __init__(self, repo: ConversationRepository, app_config: AppConfig):
        """Initialize the service"""
        self.conversation_repo = repo
        self.redis_client = get_redis_client(app_config)
        self.redis_cache_size = app_config.REDIS_CACHE_SIZE
        self.redis_entry_expiry_time_in_mins = (
            app_config.REDIS_ENTRY_EXPIRY_TIME_IN_MINS
        )
        self.vector_db_service = VectorDBService()
        self.__logger = get_logger(service_name="conversation_service")

    async def create_conversation(
        self, conversation: ConversationCreate
    ) -> ConversationRead:
        """Create a new conversation"""
        self.__logger.info(f"Creating new conversation for user {conversation.user_id}")
        saved_message = await self.conversation_repo.create_conversation(conversation)
        pydantic_obj = ConversationRead.model_validate(saved_message)
        await self.__add_entry_to_cache(conversation.user_id, pydantic_obj)

        self.__logger.info(
            f"Adding document to vector database for user {saved_message.user_id} and message {saved_message.id}"
        )
        self.vector_db_service.add_document(
            user_id=saved_message.user_id,
            message_id=saved_message.id,
            message=saved_message.message,
        )
        self.__logger.info(
            f"Document added to vector database for user {saved_message.user_id} and message {saved_message.id}"
        )
        return pydantic_obj

    async def get_user_conversations(self, user_id: int, limit: int = 20):
        """Get conversations by user"""
        self.__logger.info(f"Getting conversations for user {user_id}")
        redis_key = self.__get_cache_key(user_id)
        limit = min(limit, self.redis_cache_size)

        cached = await self.redis_client.lrange(redis_key, 0, limit - 1)

        if cached:
            self.__logger.info(f"Returning cached conversations for user {user_id}")
            return [ConversationRead(**json.loads(msg)) for msg in cached]

        self.__logger.info(
            f"No cached conversations found for user {user_id}, fetching from database"
        )
        conversations = await self.conversation_repo.get_conversations_by_user(
            user_id, limit=limit
        )

        self.__logger.info(f"Creating new cache for user {user_id}")
        await self.__create_new_cache(user_id, conversations)
        return conversations

    async def delete_user_conversations(self, user_id: int):
        """Invalidate the cache"""
        self.__logger.info(f"Invalidating cache for user {user_id}")
        await self.__invalidate_cache(user_id)

        self.__logger.info(f"Deleting conversations from database for user {user_id}")
        await self.conversation_repo.delete_conversations_by_user(user_id)

    async def __add_entry_to_cache(self, user_id: int, pydantic_obj: ConversationRead):
        """Add expiry to the cache entry"""
        self.__logger.info(f"Adding entry to cache for user {user_id}")
        redis_key = self.__get_cache_key(user_id)
        await self.redis_client.lpush(redis_key, pydantic_obj.model_dump_json())
        await self.redis_client.ltrim(redis_key, 0, self.redis_cache_size - 1)
        await self.redis_client.expire(
            redis_key, self.redis_entry_expiry_time_in_mins * 60
        )

    async def __create_new_cache(self, user_id: int, conversations: list[Conversation]):
        """Prime the cache with the new conversations"""
        redis_key = self.__get_cache_key(user_id)
        await self.__invalidate_cache(user_id)
        for convo in conversations:
            pydantic_obj = ConversationRead.model_validate(convo)
            await self.redis_client.rpush(redis_key, pydantic_obj.model_dump_json())

    async def __invalidate_cache(self, user_id: int):
        """Invalidate the cache"""
        redis_key = self.__get_cache_key(user_id)
        await self.redis_client.delete(redis_key)

    def __get_cache_key(self, user_id: int):
        """Get the cache key"""
        return f"user:{user_id}:messages"
