from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Marathon(Base):
    __tablename__ = "marathons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    photo_id = Column(String, nullable=True)
    photo_token = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)

    type = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    price = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

