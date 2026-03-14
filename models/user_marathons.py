from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class UserMarathon(Base):
    __tablename__ = "user_marathons"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    marathon_id = Column(Integer, ForeignKey("marathons.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
