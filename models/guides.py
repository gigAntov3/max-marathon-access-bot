from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from utils.database import Base

class Guide(Base):
    __tablename__ = 'guides'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Guide {self.title}>"