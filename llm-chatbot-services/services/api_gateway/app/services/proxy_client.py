"""Proxy client for the api-gateway service"""

import httpx
from fastapi import Request, Response

from shared import get_logger

logger = get_logger(service_name="api_gateway")


class ProxyClient:
    """Proxy client for the api-gateway service"""

    def __init__(self, base_url: str):
        """Initialize the proxy client"""
        self.base_url = base_url

    async def proxy_request(self, request: Request, path: str) -> Response:
        """Proxy a request to the base_url"""
        url = f"{self.base_url}{path}"

        return await self._make_request(request, url)

    async def _make_request(self, request: Request, url: str) -> Response:
        """Make a request to the base_url"""
        method = request.method

        async with httpx.AsyncClient() as client:
            proxy_response = await client.request(
                method,
                url,
                headers=request.headers.raw,
                params=request.query_params,
                content=await request.body(),
            )

        return Response(
            content=proxy_response.content,
            status_code=proxy_response.status_code,
            headers=proxy_response.headers,
        )
