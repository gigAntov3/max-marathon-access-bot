from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Mailing(Base):
    __tablename__ = "mailings"

    id = Column(Integer, primary_key=True)

    marathon_id = Column(Integer, ForeignKey("marathons.id"), nullable=True)

    title = Column(String, nullable=False)
    text = Column(String, nullable=False)

    send_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship(
        "MailingImage",
        back_populates="mailing",
        cascade="all, delete-orphan"
    )

    buttons = relationship(
        "MailingButton",
        back_populates="mailing",
        cascade="all, delete-orphan"
    )



class MailingImage(Base):
    __tablename__ = "mailing_images"

    id = Column(Integer, primary_key=True)

    mailing_id = Column(
        Integer,
        ForeignKey("mailings.id", ondelete="CASCADE"),
        nullable=False
    )

    photo_id = Column(String, nullable=False)
    photo_token = Column(String, nullable=False)
    photo_url = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    mailing = relationship(
        "Mailing",
        back_populates="images"
    )


class MailingButton(Base):
    __tablename__ = "mailing_buttons"

    id = Column(Integer, primary_key=True)

    mailing_id = Column(
        Integer,
        ForeignKey("mailings.id", ondelete="CASCADE"),
        nullable=False
    )

    text = Column(String, nullable=False)
    url = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    mailing = relationship(
        "Mailing",
        back_populates="buttons"
    )