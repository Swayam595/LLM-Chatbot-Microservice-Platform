"""Dependency factory for the API Gateway"""

from config import AppConfig
from app.services.proxy_client import ProxyClient

_app_config = AppConfig()


def get_app_config() -> AppConfig:
    """Get the app config"""
    return _app_config


def get_proxy_client(base_url: str) -> ProxyClient:
    """Get the proxy client"""
    return ProxyClient(base_url)
