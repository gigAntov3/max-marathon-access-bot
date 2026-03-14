from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Promocode(Base):
    __tablename__ = "promocodes"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    uses = Column(Integer, nullable=False, default=0)
    max_uses = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_valid(self):
        if not self.is_active:
            return False
        
        if datetime.utcnow() < self.start_date:
            return False
        
        if datetime.utcnow() > self.end_date:
            return False
        
        if self.uses >= self.max_uses:
            return False
        
        return True

