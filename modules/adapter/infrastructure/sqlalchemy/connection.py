from contextlib import asynccontextmanager
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    AsyncConnection,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeMeta

from exceptions.base import (
    NotFoundEngineErrorException,
    NotFoundMapperErrorException,
    NotFoundSessionFactoryErrorException,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import Base


class AsyncDatabase:
    def __init__(self, engine: AsyncEngine, session_factory: async_scoped_session):
        self._engine: AsyncEngine | None = engine
        self._session_factory: async_scoped_session | None = session_factory
        self._mapper: DeclarativeMeta = Base

    @property
    def engine(self) -> AsyncEngine | None:
        if not self._engine:
            raise NotFoundEngineErrorException
        return self._engine

    @property
    def session_factory(self) -> async_scoped_session | None:
        if not self._session_factory:
            raise NotFoundSessionFactoryErrorException
        return self._session_factory

    @property
    def mapper(self) -> DeclarativeMeta:
        if not self._mapper:
            raise NotFoundMapperErrorException
        return self._mapper

    async def create_all(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(self._mapper.metadata.create_all)

    async def disconnect(self) -> None:
        await self._engine.dispose()

    async def get_connection(self) -> AsyncConnection:
        return await self._engine.connect()

    @asynccontextmanager
    async def session(self) -> Callable[..., AsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
