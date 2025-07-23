"""Module for the auth service"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared import get_logger
from config import AppConfig
from app.schemas import UserCreate, UserLogin, TokenData
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.database import get_db, init_db, shutdown_db
from app.dependencies import get_current_user, require_role, validate_refresh_tokens

app_config = AppConfig()
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
    db: AsyncSession = Depends(get_db),
):  
    """Register endpoint"""
    logger.info(f"Registering user: {user.email}")
    user_repository = UserRepository(db)
    user_service = UserService(user_repository, app_config)
    return await user_service.register_user(user)

@app.post("/login")
async def login(credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login Endpoint"""
    logger.info(f"User login attempt: {credentials.email}")
    user_repository = UserRepository(db)
    user_service = UserService(user_repository, app_config)
    return await user_service.login_user(credentials)

@app.post("/refresh")
async def refresh_access_token(
    current_user: TokenData = Depends(validate_refresh_tokens), 
    db: AsyncSession = Depends(get_db),
):
    """Refresh an access token using a valid refresh token."""
    logger.info(f"Refreshing access token for user: {current_user.email}")
    user_repository = UserRepository(db)
    user_service = UserService(user_repository, app_config)
    return await user_service.refresh_access_token(current_user)

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