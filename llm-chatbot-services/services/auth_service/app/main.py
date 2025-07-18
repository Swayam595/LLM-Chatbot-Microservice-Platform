"""Module for the auth service"""
from fastapi import FastAPI
from app.schemas import UserCreate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

app = FastAPI()

# Initialize repository and service
user_repository = UserRepository()
user_service = UserService(user_repository)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Auth Service is running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/register")
def register(user: UserCreate):
    """Register a new user"""
    return user_service.register_user(user)
