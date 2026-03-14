from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class UserPromocode(Base):
    __tablename__ = "user_promocodes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"), nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="user_promocodes")
    promocode = relationship("Promocode", backref="user_promocodes")