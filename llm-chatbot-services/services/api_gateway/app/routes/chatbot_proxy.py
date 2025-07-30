"""Chatbot proxy routes"""

from fastapi import APIRouter, Request, Depends
from app.dependencies.dependency_factory import get_proxy_client, get_app_config

from shared import get_logger

logger = get_logger(service_name="api_gateway")

router = APIRouter(prefix="/chatbot", tags=["Chatbot Proxy"])

app_config = get_app_config()
chatbot_proxy_client = get_proxy_client(app_config.CHATBOT_SERVICE_URL)


@router.api_route(
    "/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def forward_to_chatbot(request: Request, full_path: str):
    """Forward a request to the chatbot service"""
    logger.info(f"Forwarding request to chatbot service: {full_path}")

    return await chatbot_proxy_client.proxy_request(request, f"/{full_path}")
