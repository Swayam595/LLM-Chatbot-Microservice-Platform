"""Module for the chatbot service"""

from fastapi import FastAPI
from app.routes import chat_router

app = FastAPI()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Chatbot Service is running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


app.include_router(chat_router)