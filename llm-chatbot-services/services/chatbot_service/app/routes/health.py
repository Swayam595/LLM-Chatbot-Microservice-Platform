"""Chatbot Service Health Check"""

import requests
from fastapi import APIRouter, HTTPException, status, Depends
from config import AppConfig
from shared import get_logger
from app.dependencies.dependency_factory import get_app_config

logger = get_logger(service_name="chatbot_service")

router = APIRouter(prefix="/health", tags=["Service Health"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
def health_check(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check endpoint"""
    logger.info("Checking health of chatbot service")
    conversation_service_health = _check_conversation_service_health(
        app_config, "health"
    )
    if conversation_service_health.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "detail": conversation_service_health.json()},
        )

    return {
        "status": "ok",
        "detail": "Chatbot service is healthy and it's dependencies are healthy",
    }


@router.get("/all", status_code=status.HTTP_200_OK, response_model=dict)
def health_check_all(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check all endpoint"""
    logger.info("Checking health of chatbot service and it's dependencies")
    conversation_service_health = _check_conversation_service_health(
        app_config, "health/all"
    )

    if conversation_service_health.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "detail": conversation_service_health.json()},
        )

    return {
        "status": "ok",
        "conversation_service_health": conversation_service_health.json(),
        "chatbot_service_health": {
            "status": "ok",
            "detail": "Chatbot service is healthy",
        },
    }


def _check_conversation_service_health(
    app_config: AppConfig, health_endpoint: str
) -> bool:
    """Check the health of the conversation service"""
    try:
        conversation_service_health_check_url = (
            f"{app_config.CONVERSATION_SERVICE_URL}/{health_endpoint}"
        )
        response = requests.get(conversation_service_health_check_url)
        return response
    except Exception as e:
        logger.error(f"Error checking conversation service health: {e}")
        return False
