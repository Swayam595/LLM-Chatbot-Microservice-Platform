"""Module for the health check endpoint"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.services.redis import get_redis_client
from app.dependencies.dependency_factory import get_app_config, get_vector_db_service
from shared import get_logger
from shared.database import get_db

logger = get_logger(service_name="conversation_service")

router = APIRouter(prefix="/health", tags=["Service Health"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check() -> dict:
    """Health check endpoint"""
    logger.info("Checking health of conversation service")

    postgres_health_status = await _check_postgres_connection()
    redis_health_status = await _check_redis_connection()
    chroma_db_health_status = _check_chroma_db_connection()

    service_health_status = _build_service_health_status(
        redis_health_status, postgres_health_status, chroma_db_health_status
    )

    if (
        not postgres_health_status["status"] == "ok"
        or not redis_health_status["status"] == "ok"
        or not chroma_db_health_status["status"] == "ok"
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=service_health_status,
        )

    return {
        "status": "ok",
        "detail": "Conversation service and its dependencies are healthy",
    }

@router.get("/all", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check_all() -> dict:
    """Health check endpoint"""
    logger.info("Checking health of conversation service")

    postgres_health_status = await _check_postgres_connection()
    redis_health_status = await _check_redis_connection()
    chroma_db_health_status = _check_chroma_db_connection()

    service_health_status = _build_service_health_status(
        redis_health_status, postgres_health_status, chroma_db_health_status
    )

    if (
        not postgres_health_status["status"] == "ok"
        or not redis_health_status["status"] == "ok"
        or not chroma_db_health_status["status"] == "ok"
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=service_health_status,
        )

    return service_health_status

async def _check_postgres_connection():
    """Check the Postgres connection"""
    postgres_health_status = {}
    try:
        logger.info("Checking Postgres connection")
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            break
        postgres_health_status["status"] = "ok"
        postgres_health_status["detail"] = "Postgres connection is healthy"
    except SQLAlchemyError as e:
        logger.error(f"Postgres connection failed. Error: {e}")
        postgres_health_status["status"] = "error"
        postgres_health_status["detail"] = str(e)
    return postgres_health_status


async def _check_redis_connection():
    """Check the Redis connection"""
    app_config = get_app_config()
    redis_health_status = dict()
    try:
        logger.info("Checking Redis connection")
        redis_client = get_redis_client(app_config)
        await redis_client.ping()
        redis_health_status["status"] = "ok"
        redis_health_status["detail"] = "Redis connection is healthy"
    except Exception as e:
        logger.error(f"Redis connection failed. Error: {e}")
        redis_health_status["status"] = "error"
        redis_health_status["detail"] = str(e)
    return redis_health_status

def _check_chroma_db_connection():
    """Check the ChromaDB connection"""
    chroma_db_health_status = {}
    vector_db_service = get_vector_db_service()
    try:
        logger.info("Checking ChromaDB connection")
        vector_db_service.client.get_or_create_collection(name="conversations")
        chroma_db_health_status["status"] = "ok"
        chroma_db_health_status["detail"] = "ChromaDB connection is healthy"
    except Exception as e:
        logger.error(f"ChromaDB connection failed. Error: {e}")
        chroma_db_health_status["status"] = "error"
        chroma_db_health_status["detail"] = str(e)
    return chroma_db_health_status


def _build_service_health_status(
    redis_health_status: dict, postgres_health_status: dict, chroma_db_health_status: dict
) -> dict:
    """Build the health status"""
    return {
        "health": {
            "conversation_service": {
                "status": "ok",
                "detail": "Conversation service is healthy",
            },
            "redis": redis_health_status,
            "postgres": postgres_health_status,
            "chroma_db": chroma_db_health_status,
        }
    }
