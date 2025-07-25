from jose import JWTError, ExpiredSignatureError
from app.repositories.refresh_token_repository import RefreshTokenRepository


async def if_expired_invalidate_token(
    token: str,
    required_token_type: str,
    refresh_token_repository: RefreshTokenRepository,
    e: JWTError,
) -> bool:
    """Invalidate the expired refresh token"""
    if isinstance(e, ExpiredSignatureError) and required_token_type == "refresh":
        await refresh_token_repository.invalidate(token)
