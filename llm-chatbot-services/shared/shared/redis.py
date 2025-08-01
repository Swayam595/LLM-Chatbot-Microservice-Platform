"""Redis client for the all services."""

import redis.asyncio as redis
from config import AppConfig

_redis_client = None

def get_redis_client(app_config: AppConfig) -> redis.Redis:
    """Get the Redis client."""
    global _redis_client
    redis_url = app_config.REDIS_URL
    if not _redis_client:   
        _redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
    return _redis_client
