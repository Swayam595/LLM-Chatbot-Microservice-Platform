"""Auth middleware"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
from config import AppConfig
from shared import get_logger
from starlette.datastructures import URL
from app.middleware.public_path import public_paths

logger = get_logger(service_name="api_gateway")


class AuthMiddleware(BaseHTTPMiddleware):
    """Auth middleware"""

    def __init__(self, app, app_config: AppConfig):
        super().__init__(app)
        self.app_config = app_config
        self._public_paths = public_paths

    async def dispatch(self, request: Request, call_next):
        """Dispatch the request"""
        if self._is_bypass_path(request):
            return await call_next(request)

        token = self._extract_token(request)
        is_valid = await self._validate_token(token)

        if not is_valid:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)

    def _extract_token(self, request: Request) -> str:
        """Extract the token from the Authorization header"""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        return auth_header.split(" ")[1]

    async def _validate_token(self, token: str) -> bool:
        """Validate the token"""
        if not token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"URL: {self.app_config.AUTH_SERVICE_URL}/me")
                response = await client.get(
                    f"{self.app_config.AUTH_SERVICE_URL}/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=3.0,
                )
                return response.status_code == 200
        except httpx.RequestError as e:
            logger.error(f"Auth-service unreachable: {e}")
            return JSONResponse(
                status_code=503,
                content={"detail": "Authentication service unavailable"},
            )

    def _is_bypass_path(self, request: Request) -> bool:
        """Check if the path is a bypass path"""
        normalized_path = str(URL(request.url.path).path.rstrip("/"))
        return (request.method, normalized_path) in self._public_paths
