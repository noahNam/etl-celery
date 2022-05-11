from contextlib import asynccontextmanager
from typing import Callable, AsyncContextManager, List, Type

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    AsyncConnection,
    AsyncSession,
)
from sqlalchemy.future import Engine as SyncEngine
from sqlalchemy.orm import DeclarativeMeta, scoped_session

from exceptions.base import (
    NotFoundEngineErrorException,
    NotFoundMapperErrorException,
    NotFoundSessionFactoryErrorException,
)


class AsyncDatabase:
    def __init__(
        self,
        engine_list: List[AsyncEngine | None],
        session_factory: async_scoped_session,
        mapper_list: List[Type[DeclarativeMeta]],
    ):
        self._engines: List[AsyncEngine | None] = engine_list
        self._session_factory: async_scoped_session | None = session_factory
        self._mappers: List[Type[DeclarativeMeta]] = mapper_list

    @property
    def engines(self) -> List[AsyncEngine | None]:
        if not self._engines:
            raise NotFoundEngineErrorException
        return self._engines

    @property
    def session_factory(self) -> async_scoped_session | None:
        if not self._session_factory or not isinstance(self._session_factory, async_scoped_session):
            raise NotFoundSessionFactoryErrorException
        return self._session_factory

    @property
    def mappers(self) -> List[Type[DeclarativeMeta]]:
        if not self._mappers:
            raise NotFoundMapperErrorException
        return self._mappers

    async def create_all(self) -> None:
        if not self._engines:
            raise NotFoundEngineErrorException
        if not self._mappers:
            raise NotFoundMapperErrorException

        for engine, mapper in zip(self._engines, self._mappers):
            async with engine.begin() as connection:
                await connection.run_sync(mapper.metadata.create_all)

    async def disconnect(self) -> None:
        for engine in self._engines:
            await engine.dispose()

    async def get_connection_list(self) -> List[AsyncConnection]:
        connection_list = list()
        for engine in self._engines:
            connection_list.append(await engine.connect())
        return connection_list

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


class SyncDatabase:
    def __init__(
        self,
        engine_list: List[SyncEngine | None],
        session_factory: scoped_session,
        mapper_list: List[Type[DeclarativeMeta]],
    ):
        self._engines: List[SyncEngine | None] = engine_list
        self._session_factory: scoped_session | None = session_factory
        self._mappers: List[Type[DeclarativeMeta]] = mapper_list

    @property
    def engines(self) -> List[SyncEngine | None]:
        if not self._engines:
            raise NotFoundEngineErrorException
        return self._engines

    @property
    def session_factory(self) -> scoped_session | None:
        if not self._session_factory or not isinstance(self._session_factory, scoped_session):
            raise NotFoundSessionFactoryErrorException
        return self._session_factory

    @property
    def mappers(self) -> List[Type[DeclarativeMeta]]:
        if not self._mappers:
            raise NotFoundMapperErrorException
        return self._mappers

    async def create_all(self) -> None:
        if not self._engines:
            raise NotFoundEngineErrorException
        if not self._mappers:
            raise NotFoundMapperErrorException

        for engine, mapper in zip(self._engines, self._mappers):
            with engine.begin():
                mapper.metadata.create_all()
