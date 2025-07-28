"""Redis client for the conversation service."""

import redis.asyncio as redis
from shared import get_logger
from config import AppConfig

logger = get_logger(service_name="conversation_service")

_redis_client = None


def get_redis_client(app_config: AppConfig) -> redis.Redis:
    """Get the Redis client."""
    global _redis_client
    redis_url = app_config.REDIS_URL
    if not _redis_client:
        logger.info("Connecting to Redis...")
        _redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
    return _redis_client
