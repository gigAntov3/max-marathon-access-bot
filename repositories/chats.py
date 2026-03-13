from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.chats import Chat
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class ChatsRepository(SQLAlchemyRepository):
    model = Chat