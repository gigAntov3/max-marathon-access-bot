from typing import Optional

from abc import ABC, abstractmethod

from sqlalchemy import and_, insert, select, update, delete

from sqlalchemy import asc, desc

from utils.database import db_helper


class BaseRepository(ABC):

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError
    

class SQLAlchemyRepository(BaseRepository):
    model = None   

    async def add_one(self, **kwargs) -> object:
        async with db_helper.get_session() as session:
            stmt = (
                insert(self.model)
                .values(**kwargs)
                .returning(self.model.id)
            )
            result = await session.execute(stmt)
            new_id = result.scalar_one()
            await session.commit()

            # Получаем полную модель по id
            query = select(self.model).where(self.model.id == new_id)
            result = await session.execute(query)
            return result.scalar_one()
        

    async def get_one(self, id: int) -> Optional[object]:
        async with db_helper.get_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()
        
    async def find_one(self, order_by: str = "asc", **kwargs):
        async with db_helper.get_session() as session:
            if order_by == "desc":
                stmt = select(self.model).order_by(desc(self.model.id)).filter_by(**kwargs)
            else:
                stmt = select(self.model).order_by(asc(self.model.id)).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.scalars().first()
        

    async def find_all(self, offset: int = 0, limit: int = 10, **kwargs) -> list:
        async with db_helper.get_session() as session:
            stmt = select(self.model).filter_by(**kwargs).order_by(desc(self.model.id)).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
        

    async def update_one(self, id: int, **kwargs):
        async with db_helper.get_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**kwargs)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            updated_obj = result.scalar_one_or_none()
            return updated_obj
        


    async def delete_one(self, id: int):
        async with db_helper.get_session() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()


    async def delete_all(self, **kwargs):
        async with db_helper.get_session() as session:
            stmt = delete(self.model).filter_by(**kwargs)
            await session.execute(stmt)
            await session.commit()