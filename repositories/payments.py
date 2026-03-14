from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.payments import Payment
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class PaymentsRepository(SQLAlchemyRepository):
    model = Payment