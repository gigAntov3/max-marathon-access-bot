from typing import AsyncGenerator
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine, 
    async_sessionmaker
)

from models.base import Base
from config.settings import settings


class DatabaseHelper:
    def __init__(
            self, 
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            # pool_size: int = 5,
            # max_overflow: int = 10,
        ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url, 
            echo=echo, 
            echo_pool=echo_pool, 
            # pool_size=pool_size, 
            # max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    def get_session(self) -> AsyncContextManager[AsyncSession]:
        """
        Возвращает асинхронный контекстный менеджер для работы с сессией.
        Использовать так:
            async with db_helper.get_session() as session:
                ...
        """
        return self.session_factory()
    
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(
    url=settings.database.url,
    echo=settings.database.echo,
    echo_pool=settings.database.echo_pool,
    # pool_size=settings.database.pool_size,
    # max_overflow=settings.database.max_overflow
)