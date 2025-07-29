"""Module for the chatbot service"""

from fastapi import FastAPI
from shared import get_logger
from app.routes import chat_router, health_router

logger = get_logger(service_name="chatbot_service")

logger.info("Chatbot Service is up and running.")

app = FastAPI()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Chatbot Service is running"}


app.include_router(chat_router)
app.include_router(health_router)
