"""Module for the auth service"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared import get_logger
from config import AppConfig

from app.services.refresh_token_service import RefreshTokenService
from app.schemas import UserCreate, UserLogin, TokenData
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.database import get_db, init_db, shutdown_db
from app.dependencies import get_current_user, require_role, validate_refresh_tokens
from app.dependencies.dependency_factory import (
    get_app_config,
    get_user_service,
    get_user_repository,
)

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
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """Register endpoint"""
    logger.info(f"Registering user: {user.email}")
    return await user_service.register_user(user)


@app.post("/login")
async def login(
    credentials: UserLogin,
    user_service: UserService = Depends(get_user_service),
):
    """Login Endpoint"""
    logger.info(f"User login attempt: {credentials.email}")
    return await user_service.login_user(credentials)


@app.post("/refresh")
async def refresh_access_token(
    current_user: TokenData = Depends(validate_refresh_tokens),
    user_repository: UserRepository = Depends(get_user_repository),
    app_config: AppConfig = Depends(get_app_config),
):
    """Refresh an access token using a valid refresh token."""
    logger.info(f"Refreshing access token for user: {current_user.email}")
    refresh_token_service = RefreshTokenService(app_config, user_repository)
    return await refresh_token_service.get_new_tokens(current_user)


@app.get("/me")
async def read_current_user(
    current_user: TokenData = Depends(get_current_user),
):
    """Protected endpoint"""
    logger.info(f"Reading current user: {current_user.email}")
    return {"message": "Registered user", "user": current_user}


@app.get("/admin-only")
async def admin_dashboard(current_user=Depends(require_role("admin"))):
    """Admin dashboard"""
    logger.info(f"Admin accessed by {current_user.email}")
    return {"message": f"Welcome, admin {current_user.email}"}
