"""Health check endpoints for the auth service"""

from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from shared import get_logger
from app.dependencies.dependency_factory import get_db_session

logger = get_logger(service_name="auth_service")

router = APIRouter(prefix="/health", tags=["Service Health"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check() -> dict:
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    database_health = await _check_postgres_connection()

    _raise_exception_if_dependency_service_is_unhealthy(database_health)
    logger.info("Auth Service and it's dependencies are healthy")

    return {
        "status": "ok",
        "detail": "Auth Service is healthy and it's dependencies are healthy",
    }

@router.get("/all", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check_all() -> dict:
    """Health check all endpoint"""
    logger.info("Health check all endpoint called")
    database_health = await _check_postgres_connection()

    _raise_exception_if_dependency_service_is_unhealthy(database_health)
    logger.info("Auth Service and postgres connection are healthy")

    return {
        "status": "ok",
        "auth_service_health": {
            "status": "ok",
            "detail": "Auth Service is healthy",
        },
        "database_health": database_health,
    }


async def _check_postgres_connection():
    """Check the Postgres connection"""
    postgres_health_status = {}
    try:
        logger.info("Checking Postgres connection")
        db = await get_db_session()
        await db.execute(text("SELECT 1"))
        postgres_health_status["status"] = "ok"
        postgres_health_status["detail"] = "Postgres connection is healthy"
    except SQLAlchemyError as e:
        logger.error(f"Postgres connection failed. Error: {e}")
        postgres_health_status["status"] = "error"
        postgres_health_status["detail"] = str(e)
    return postgres_health_status

def _raise_exception_if_dependency_service_is_unhealthy(postgres_health_status: dict) -> None:
    """Raise an exception if the Postgres connection is unhealthy"""
    if not postgres_health_status["status"] == "ok":
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=postgres_health_status["detail"])