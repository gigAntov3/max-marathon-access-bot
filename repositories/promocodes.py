from datetime import datetime
from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.promocodes import Promocode
from models.use_promocodes import UsePromocode
from repositories.base import SQLAlchemyRepository
from utils.database import db_helper


class PromocodesRepository(SQLAlchemyRepository):
    model = Promocode

    async def increment_uses(self, promocode_id: int):
        async with db_helper.get_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == promocode_id)
                .values(uses=func.uses + 1)
            )
            await session.execute(stmt)
            await session.commit()

    async def is_valid(self, code: str) -> bool:
        """Проверяет существует ли промокод, активен ли он, не превышено ли max_uses, и актуальна ли дата."""
        async with db_helper.get_session() as session:
            stmt = select(self.model).where(self.model.code == code)
            result = await session.execute(stmt)
            promocode: Promocode | None = result.scalars().one_or_none()
            if not promocode:
                return False
            now = datetime.utcnow()
            return (
                promocode.is_active and
                promocode.uses < promocode.max_uses and
                promocode.start_date <= now <= promocode.end_date
            )

    async def use_promocode(self, user_id: int, promocode_id: int):
        """Привязывает промокод к пользователю и увеличивает счетчик использований."""
        async with db_helper.get_session() as session:
            try:
                # Проверка, не использовал ли пользователь этот промокод
                stmt_check = select(UsePromocode).where(
                    UsePromocode.user_id == user_id,
                    UsePromocode.promocode_id == promocode_id
                )
                result = await session.execute(stmt_check)
                existing = result.scalars().first()
                if existing:
                    return False  # Уже использовал

                # Создаем запись о использовании
                new_use = UsePromocode(user_id=user_id, promocode_id=promocode_id)
                session.add(new_use)

                # Увеличиваем счетчик использований
                stmt_update = (
                    update(Promocode)
                    .where(Promocode.id == promocode_id)
                    .values(uses=Promocode.uses + 1)
                )
                await session.execute(stmt_update)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                return False