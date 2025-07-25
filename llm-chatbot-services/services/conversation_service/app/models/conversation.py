"""Module for the conversation model"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from shared import Base

class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
