"""Rate limiter middleware"""

import time
import redis.asyncio as redis
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from shared import get_logger


class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiter middleware"""

    def __init__(
        self, app, redis_client: redis.Redis, limit: int = 100, window: int = 60
    ):
        """Initialize the rate limiter middleware"""
        super().__init__(app)
        self.redis = redis_client
        self.limit = limit
        self.window = window
        self.logger = get_logger(service_name="api_gateway")

    async def dispatch(self, request: Request, call_next):
        """Dispatch the request"""
        self.logger.info(f"Dispatching request: {request.method} {request.url}")
        ip = self._get_ip(request)
        key = f"ratelimit:{ip}"

        current_ts = int(time.time())

        pipe = self.redis.pipeline()
        pipe.zadd(key, {str(current_ts): current_ts})
        pipe.zremrangebyscore(key, 0, current_ts - self.window)
        pipe.zcard(key)
        pipe.expire(key, self.window + 1)
        _, _, count, _ = await pipe.execute()

        if count > self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": f"Rate limit exceeded. Try again in a few seconds."},
            )

        return await call_next(request)

    def _get_ip(self, request: Request):
        return request.headers.get("X-Forwarded-For", request.client.host)
