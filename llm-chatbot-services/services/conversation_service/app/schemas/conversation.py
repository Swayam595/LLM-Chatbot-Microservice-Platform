"""Conversation Service Schemas"""
from datetime import datetime
from pydantic import BaseModel

class ConversationCreate(BaseModel):
    """Create a new conversation"""
    user_id: int
    message: str

class ConversationRead(BaseModel):
    """Read a conversation"""
    id: int
    user_id: int
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
