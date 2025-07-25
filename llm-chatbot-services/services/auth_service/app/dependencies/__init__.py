"""Module for the auth dependencies"""

from .roles import require_role
from .dependency_factory import (
    get_user_repository,
    get_user_service,
    get_app_config,
    get_refresh_token_repository,
    get_reset_password_service,
)

__all__ = [
    "require_role",
    "get_user_repository",
    "get_user_service",
    "get_app_config",
    "get_refresh_token_repository",
    "get_reset_password_service",
]
