from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from models.users import User
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