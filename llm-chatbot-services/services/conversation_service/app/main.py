"""Module for the conversation service"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from shared.database import init_db, shutdown_db
from shared.logger import get_logger
from app.routes import conversation_router, health_router

logger = get_logger(service_name="conversation-service")
logger.info("Starting Conversation Service")


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    """Lifespan for the application"""
    logger.info("Initializing database")
    await init_db()
    yield
    logger.info("Shutting down database")
    await shutdown_db()


app = FastAPI(lifespan=lifespan)

app.include_router(conversation_router)
app.include_router(health_router)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Conversation Service is running"}
