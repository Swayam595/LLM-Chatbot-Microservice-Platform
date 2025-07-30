"""Health check endpoints for the API Gateway"""

import requests
from fastapi import APIRouter, status, Depends, HTTPException
from shared import get_logger
from config import AppConfig
from app.dependencies.dependency_factory import get_app_config

logger = get_logger(service_name="api_gateway")

router = APIRouter(prefix="/health", tags=["Service Health"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check endpoint"""
    logger.info("Checking health of API Gateway")
    auth_service_health = _check_auth_service_health(app_config)
    chatbot_service_health = _check_chatbot_service_health(app_config)
    conversation_service_health = _check_conversation_service_health(app_config)

    _raise_exception_if_any_service_is_unhealthy(auth_service_health, chatbot_service_health, conversation_service_health)

    return {
        "status": "ok",
        "detail": "API Gateway is healthy and it's dependencies are healthy",
    }


@router.get("/all", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check_all(app_config: AppConfig = Depends(get_app_config)) -> dict:
    """Health check all endpoint"""
    logger.info("Checking health of all services")
    auth_service_health = _check_auth_service_health(app_config, "all")
    chatbot_service_health = _check_chatbot_service_health(app_config, "all")
    conversation_service_health = _check_conversation_service_health(app_config, "all")

    _raise_exception_if_any_service_is_unhealthy(auth_service_health, chatbot_service_health, conversation_service_health)

    return {
        "status": "ok",
        "api_gateway_health": {
            "status": "ok",
            "detail": "API Gateway is healthy",
        },
        "auth_service_health": auth_service_health.json(),
        "chatbot_service_health": chatbot_service_health.json(),
        "conversation_service_health": conversation_service_health.json(),
    }

def _check_auth_service_health(app_config: AppConfig, health_endpoint: str = None) -> dict:
    """Check the health of the auth service"""
    logger.info("Checking health of auth service")
    auth_service_url = app_config.AUTH_SERVICE_URL
    response = _make_request(auth_service_url, "GET", {}, health_endpoint)
    return response

def _check_chatbot_service_health(app_config: AppConfig, health_endpoint: str = None) -> dict:
    """Check the health of the chatbot service"""
    logger.info("Checking health of chatbot service")
    chatbot_service_url = app_config.CHATBOT_SERVICE_URL
    response = _make_request(chatbot_service_url, "GET", {}, health_endpoint)
    return response

def _check_conversation_service_health(app_config: AppConfig, health_endpoint: str = None) -> dict:
    """Check the health of the conversation service"""
    logger.info("Checking health of conversation service")
    conversation_service_url = app_config.CONVERSATION_SERVICE_URL
    response = _make_request(conversation_service_url, "GET", {}, health_endpoint)
    return response


def _make_request(url: str, method: str, json: dict, health_endpoint: str = None) -> requests.Response:
    """Make a request to the given url"""
    try:
        health_url = f"{url}/health" 
        if health_endpoint:
            health_url = f"{health_url}/{health_endpoint}"
        logger.info(f"Making request to service health endpoint {health_url} with method {method} and json {json}")
        response = requests.request(method, health_url, json=json)
        return response
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(f"Error making request to {url}: {e}")
        _throw_exception(500, str(e))

def _raise_exception_if_any_service_is_unhealthy(auth_service_health: requests.Response, 
                                                chatbot_service_health: requests.Response, 
                                                conversation_service_health: requests.Response,) -> None:
    """Raise an exception if any service is unhealthy"""
    if (
        auth_service_health.status_code != 200
        or chatbot_service_health.status_code != 200
        or conversation_service_health.status_code != 200
    ):
        raise HTTPException(
            status_code=500,
            detail=_construct_error_detail(
                auth_service_health,
                chatbot_service_health,
                conversation_service_health,
            ),
        )

def _construct_error_detail(auth_service_health: requests.Response, chatbot_service_health: requests.Response, conversation_service_health: requests.Response) -> dict:
    """Construct the error detail"""
    return {
        "auth_service_health": auth_service_health.json(),
        "chatbot_service_health": chatbot_service_health.json(),
        "conversation_service_health": conversation_service_health.json(),
    }

def _throw_exception(status_code: int, detail: str) -> HTTPException:
    """Throw an exception"""
    raise HTTPException(
        status_code=status_code,
        detail={"status": "error", "detail": detail},
    )
