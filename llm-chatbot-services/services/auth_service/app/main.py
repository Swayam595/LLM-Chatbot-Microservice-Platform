"""Module for the auth service"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from shared import get_logger
from config import AppConfig

from app.services.refresh_token_service import RefreshTokenService
from app.schemas import (
    UserCreate,
    UserLogin,
    TokenData,
    ValidatedToken,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.user_service import UserService
from app.services.database import init_db, shutdown_db
from app.dependencies import (
    require_role,
    get_refresh_token_repository,
)
from app.dependencies.authentication import (
    get_current_user,
    validate_refresh_token,
    validate_forgot_password_token,
)
from app.dependencies.dependency_factory import (
    get_app_config,
    get_user_repository,
    get_user_service,
    get_reset_password_service,
)
from app.services.reset_password_service import ResetPasswordService

logger = get_logger(service_name="auth_service")


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    """Lifespan for the application"""
    logger.info("Initializing database")
    await init_db()
    yield
    logger.info("Shutting down database")
    await shutdown_db()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    """Root endpoint"""
    logger.info("Root endpoint called")
    return {"message": "Auth Service is running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check called")
    return {"status": "ok"}


@app.post("/register")
async def register(
    user: UserCreate, user_service: UserService = Depends(get_user_service),
):
    """Register endpoint"""
    logger.info(f"Registering user: {user.email}")
    return await user_service.register_user(user)


@app.post("/login")
async def login(
    credentials: UserLogin, user_service: UserService = Depends(get_user_service),
):
    """Login Endpoint"""
    logger.info(f"User login attempt: {credentials.email}")
    return await user_service.login_user(credentials)


@app.post("/logout")
async def logout(
    validated_token: ValidatedToken = Depends(validate_refresh_token),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
):
    """Logout endpoint"""
    logger.info(f"Logging out user: {validated_token.email}")
    await refresh_token_repository.invalidate(validated_token.token)
    return {"message": f"{validated_token.email} logged out successfully"}


@app.post("/refresh")
async def refresh_access_token(
    current_user: TokenData = Depends(validate_refresh_token),
    user_repository: UserRepository = Depends(get_user_repository),
    app_config: AppConfig = Depends(get_app_config),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
):
    """Refresh an access token using a valid refresh token."""
    logger.info(f"Refreshing access token for user: {current_user.email}")
    refresh_token_service = RefreshTokenService(
        app_config, user_repository, refresh_token_repository
    )
    return await refresh_token_service.get_new_tokens(current_user)


@app.post("/forgot-password")
async def forgot_password(
    forgot_password_data: ForgotPasswordRequest,
    reset_password_service: ResetPasswordService = Depends(get_reset_password_service),
):
    """Forgot password endpoint"""
    logger.info(
        f"Forgot password endpoint called for user: {forgot_password_data.email}"
    )
    return await reset_password_service.get_reset_password_token(forgot_password_data)


@app.post("/reset-password")
async def reset_password(
    reset_password_data: ResetPasswordRequest,
    app_config: AppConfig = Depends(get_app_config),
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
    reset_password_service: ResetPasswordService = Depends(get_reset_password_service),
):
    """Reset password endpoint"""
    logger.info("Reset password endpoint called")
    token_data: TokenData = await validate_forgot_password_token(
        reset_password_data.reset_password_token,
        app_config,
        user_repository,
        refresh_token_repository,
    )
    return await reset_password_service.reset_password(
        token_data.email, reset_password_data
    )


@app.get("/me")
async def read_current_user(current_user: TokenData = Depends(get_current_user),):
    """Protected endpoint"""
    logger.info(f"Reading current user: {current_user.email}")
    return {"message": "Registered user", "user": current_user}


@app.get("/admin-only")
async def admin_dashboard(current_user=Depends(require_role("admin"))):
    """Admin dashboard"""
    logger.info(f"Admin dashboard accessed by {current_user.email}")
    return {"message": f"Welcome, admin {current_user.email}"}
