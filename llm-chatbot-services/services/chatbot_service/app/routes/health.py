"""Chatbot Service Health Check"""

import requests
from fastapi import APIRouter, HTTPException, status, Depends
from shared import get_logger
from config import AppConfig
from app.dependencies.dependency_factory import get_app_config
from app.llm.factory import get_llm_provider

logger = get_logger(service_name="chatbot_service")

router = APIRouter(prefix="/health", tags=["Service Health"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check endpoint"""
    logger.info("Checking health of chatbot service")
    conversation_service_health = _check_conversation_service_health(
        app_config
    )

    llm_api_health, llm_provider_name = await _check_llm_api_health()
    
    if conversation_service_health.status_code != 200 or llm_api_health.status_code != 200:
        _throw_exception(503, detail = {
            "conversation_service_health": conversation_service_health.json(),
            f"{llm_provider_name} API health": llm_api_health.json()
        })

    return {
        "status": "ok",
        "detail": "Chatbot service is healthy and it's dependencies are healthy",
    }


@router.get("/all", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check_all(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check all endpoint"""
    logger.info("Checking health of chatbot service and it's dependencies")
    conversation_service_health = _check_conversation_service_health(
        app_config, "/all"
    )

    llm_api_health, llm_provider_name = await _check_llm_api_health()

    if conversation_service_health.status_code != 200 or llm_api_health.status_code != 200:
        _throw_exception(503, detail = {
            "conversation_service_health": conversation_service_health.json(),
            f"{llm_provider_name} API health": llm_api_health.json()
        })

    return {
        "status": "ok",
        "conversation_service_health": conversation_service_health.json(),
        "chatbot_service_health": {
            "status": "ok",
            "detail": "Chatbot service is healthy",
        },
        "llm_api_health": {
            "status": "ok",
            "detail": f"{llm_provider_name} API is healthy",
        }
    }


def _check_conversation_service_health(
    app_config: AppConfig, health_endpoint: str = None
) -> requests.Response | HTTPException:
    """Check the health of the conversation service"""
    conversation_service_health_check_url = (
            f"{app_config.CONVERSATION_SERVICE_URL}/health"
        )
    if health_endpoint is not None:
        conversation_service_health_check_url = f"{conversation_service_health_check_url}{health_endpoint}"
    
    return _make_request(conversation_service_health_check_url, "GET", {})

async def _check_llm_api_health() -> requests.Response | HTTPException:
    """Check the health of the gemini api"""
    llm_provider = get_llm_provider()
    response = await llm_provider.generate_response("Hello, how are you?")
    return response, llm_provider.llm_name

def _make_request(url: str, method: str, json: dict) -> requests.Response:
    """Make a request to the given url"""
    try:
        response = requests.request(method, url, json=json)
        return response
    except Exception as e: #pylint: disable=broad-exception-caught
        logger.error(f"Error making request to {url}: {e}")
        _throw_exception(500, str(e))

def _throw_exception(status_code: int, detail: str) -> HTTPException:
    """Throw an exception"""
    raise HTTPException(
        status_code=status_code,
        detail={"status": "error", "detail": detail},
    )
