from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    marathon_id = Column(Integer, ForeignKey("marathons.id"), nullable=False)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"), nullable=True)

    amount = Column(Float, nullable=False)
    discount_amount = Column(Float, nullable=True, default=0)
    status = Column(String, nullable=False, default="pending")
    payment_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="payments")
    marathon = relationship("Marathon", backref="payments")
    promocode = relationship("Promocode", backref="payments")