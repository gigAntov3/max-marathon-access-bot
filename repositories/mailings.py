from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from models.mailings import Mailing, MailingImage, MailingButton
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class MailingsRepository(SQLAlchemyRepository):
    model = Mailing


    async def get_full(self, id: int) -> Mailing | None:
        async with db_helper.get_session() as session:

            query = (
                select(Mailing)
                .where(Mailing.id == id)
                .options(
                    selectinload(Mailing.images),
                    selectinload(Mailing.buttons),
                )
            )

            result = await session.execute(query)

            return result.scalar_one_or_none()


class MailingImageRepository(SQLAlchemyRepository):
    model = MailingImage


class MailingButtonRepository(SQLAlchemyRepository):
    model = MailingButton