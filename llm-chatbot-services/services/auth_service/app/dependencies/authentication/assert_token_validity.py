from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository


def assert_token_payload_has_required_fields(payload: dict) -> bool:
    """Assert the token payload is valid"""
    if not _are_required_token_payload_fields_present(payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


def assert_token_payload_is_required_token_type(
    payload: dict, required_token_type: str
) -> bool:
    """Assert the token payload is the required token type"""
    if not _is_token_type_is_required_token_type(payload, required_token_type):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def assert_valid_user_exists(email: str, user_repository: UserRepository) -> bool:
    """Assert the user exists"""
    if not await _is_user_present(email, user_repository):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token provided.User {email} not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _are_required_token_payload_fields_present(payload: dict) -> bool:
    """Assert the token payload has required fields"""
    email = payload.get("sub")
    role = payload.get("role")
    return email is not None and role is not None


def _is_token_type_is_required_token_type(
    payload: dict, required_token_type: str
) -> bool:
    """Check if the token type is the required token type"""
    token_type = payload.get("type")
    return token_type == required_token_type


async def _is_user_present(email: str, user_repository: UserRepository) -> bool:
    """Check if the user is present"""
    user = await user_repository.get_user_by_email(email)
    return user is not None
