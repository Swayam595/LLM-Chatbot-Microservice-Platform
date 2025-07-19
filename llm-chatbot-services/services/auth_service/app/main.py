"""Module for the auth service"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import AppConfig
from app.schemas import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.database import get_db, init_db, shutdown_db

app_config = AppConfig()

@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    """Lifespan for the application"""
    await init_db()
    yield
    await shutdown_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Auth Service is running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/register")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):  
    """Register endpoint"""
    user_repository = UserRepository(db)
    user_service = UserService(user_repository, app_config)
    return await user_service.register_user(user)

@app.post("/login")
async def login(credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login Endpoint"""
    user_repository = UserRepository(db)
    user_service = UserService(user_repository, app_config)
    return await user_service.login_user(credentials)

