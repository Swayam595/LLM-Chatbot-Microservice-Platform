"""Schemas for the chat service"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request schema for the chat service"""

    user_id: int
    message: str


class ChatResponse(BaseModel):
    """Response schema for the chat service"""

    response: str
