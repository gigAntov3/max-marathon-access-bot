from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.guides import Guide
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class GuidesRepository(SQLAlchemyRepository):
    model = Guide