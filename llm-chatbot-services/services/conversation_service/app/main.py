"""Module for the conversation service"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Conversation Service is running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
