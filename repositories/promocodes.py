from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.promocodes import Promocode
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class PromocodesRepository(SQLAlchemyRepository):
    model = Promocode