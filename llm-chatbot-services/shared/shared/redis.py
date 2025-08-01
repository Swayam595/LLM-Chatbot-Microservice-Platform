"""Redis client for the all services."""

import redis.asyncio as redis
from .base_config import BaseAppConfig
import threading


class RedisClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, app_config: BaseAppConfig):
        if not hasattr(self, "initialized"):
            self.app_config = app_config
            self.redis_client = None
            self.initialized = True

    def get_redis_client(self) -> redis.Redis:
        if not self.redis_client:
            self.redis_client = redis.Redis.from_url(self.app_config.REDIS_URL, decode_responses=True)
        return self.redis_client