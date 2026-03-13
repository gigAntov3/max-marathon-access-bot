from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    marathon_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    link = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

