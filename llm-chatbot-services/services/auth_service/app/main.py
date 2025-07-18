"""Module for the auth service"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.database import get_db, init_db, shutdown_db

@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    """Lifespan for the application"""
    await init_db()
    yield
    await shutdown_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    """Health check endpoint"""
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
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.register_user(user)
