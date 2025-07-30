"""Conversation proxy routes"""

from fastapi import APIRouter, Request, Depends
from app.dependencies.dependency_factory import get_proxy_client, get_app_config

from shared import get_logger

logger = get_logger(service_name="api_gateway")

router = APIRouter(prefix="/conversation", tags=["Conversation Proxy"])

app_config = get_app_config()
conversation_proxy_client = get_proxy_client(app_config.CONVERSATION_SERVICE_URL)


@router.api_route(
    "/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def forward_to_conversation(request: Request, full_path: str):
    """Forward a request to the conversation service"""
    logger.info(f"Forwarding request to conversation service: {full_path}")

    return await conversation_proxy_client.proxy_request(request, f"/{full_path}")
