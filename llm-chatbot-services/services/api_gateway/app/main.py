"""Module for the api-gateway service"""

from fastapi import FastAPI
from redis.asyncio import Redis
from shared import get_logger, RedisClient
from app.dependencies.dependency_factory import get_app_config
from app.routes import (
    health_router,
    auth_proxy_router,
    chatbot_proxy_router,
    conversation_proxy_router,
)
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limiter import RedisRateLimitMiddleware

logger = get_logger(service_name="api_gateway")
app_config = get_app_config()
redis_client = RedisClient(app_config).get_redis_client()


app = FastAPI()
app.add_middleware(AuthMiddleware, app_config=app_config)
app.add_middleware(
    RedisRateLimitMiddleware, redis_client=redis_client, limit=100, window=60
)


logger.info("API Gateway service is up and running.")


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Api-Gateway Service is running"}


app.include_router(health_router)
app.include_router(auth_proxy_router)
app.include_router(chatbot_proxy_router)
app.include_router(conversation_proxy_router)


# Setup Redis client
redis_client = Redis.from_url("redis://redis:6379", decode_responses=True)

# Add middleware to app
