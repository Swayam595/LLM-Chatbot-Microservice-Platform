"""Module for the api-gateway service"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Api-Gateway Service is running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
