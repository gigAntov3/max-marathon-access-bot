from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.marathons import Marathon
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class MarathonsRepository(SQLAlchemyRepository):
    model = Marathon