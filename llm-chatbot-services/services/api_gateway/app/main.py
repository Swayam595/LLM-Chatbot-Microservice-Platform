"""Module for the api-gateway service"""

from fastapi import FastAPI
from shared import get_logger
from app.routes import (
    health_router,
    auth_proxy_router,
    chatbot_proxy_router,
    conversation_proxy_router,
)

logger = get_logger(service_name="api_gateway")

app = FastAPI()

logger.info("API Gateway service is up and running.")


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Api-Gateway Service is running"}


app.include_router(health_router)
app.include_router(auth_proxy_router)
app.include_router(chatbot_proxy_router)
app.include_router(conversation_proxy_router)
