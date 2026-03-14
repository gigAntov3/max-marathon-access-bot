from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.users import User
from models.user_marathons import UserMarathon
from models.marathons import Marathon
from repositories.base import SQLAlchemyRepository

from utils.database import db_helper


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def get_or_create(
        self, 
        user_id: int,
        first_name: str, 
        last_name: str | None,
        username: str | None,
    ) -> User:
        async with db_helper.get_session() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user:
                return user

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                user_id=user_id,
            )

            session.add(new_user)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                result = await session.execute(query)
                new_user = result.scalar_one()
            
            return new_user
        

    async def update_phone_by_user_id(self, user_id: int, phone: str):
        async with db_helper.get_session() as session:
            stmt = update(User).where(User.user_id == user_id).values(phone=phone)
            await session.execute(stmt)
            await session.commit()


    async def add_marathon_to_user(self, user_id: int, marathon_id: int):
        async with db_helper.get_session() as session:
            stmt = select(UserMarathon).where(
                UserMarathon.user_id == user_id,
                UserMarathon.marathon_id == marathon_id
            )

            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                return existing

            user_marathon = UserMarathon(
                user_id=user_id,
                marathon_id=marathon_id
            )

            session.add(user_marathon)

            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                result = await session.execute(stmt)
                user_marathon = result.scalar_one()

            return user_marathon
        
    async def get_user_marathons(self, user_id: int):
        async with db_helper.get_session() as session:
            stmt = (
                select(Marathon)
                .join(UserMarathon, UserMarathon.marathon_id == Marathon.id)
                .where(UserMarathon.user_id == user_id)
            )

            result = await session.execute(stmt)

            return result.scalars().all()