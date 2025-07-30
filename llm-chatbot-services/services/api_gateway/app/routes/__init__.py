from .health import router as health_router
from .auth_proxy import router as auth_proxy_router
from .chatbot_proxy import router as chatbot_proxy_router
from .conversation_proxy import router as conversation_proxy_router

__all__ = [
    "health_router",
    "auth_proxy_router",
    "chatbot_proxy_router",
    "conversation_proxy_router",
]
