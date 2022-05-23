from contextlib import asynccontextmanager, contextmanager
from typing import Callable, AsyncContextManager, Type, ContextManager

from sqlalchemy.engine import Transaction
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    AsyncConnection,
    AsyncSession,
)
from sqlalchemy.future import Engine as SyncEngine, Connection as SyncConnection
from sqlalchemy.orm import DeclarativeMeta, scoped_session, Session

from exceptions.base import (
    NotFoundEngineErrorException,
    NotFoundMapperErrorException,
    NotFoundSessionFactoryErrorException,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class AsyncDatabase:
    def __init__(
        self,
        engine_list: list[AsyncEngine | None],
        session_factory: async_scoped_session,
        mapper_list: list[Type[DeclarativeMeta]],
    ):
        self._engines: list[AsyncEngine | None] = engine_list
        self._session_factory: async_scoped_session | None = session_factory
        self._mappers: list[Type[DeclarativeMeta]] = mapper_list

    @property
    def engines(self) -> list[AsyncEngine | None]:
        if not self._engines:
            raise NotFoundEngineErrorException
        return self._engines

    @property
    def session_factory(self) -> async_scoped_session | None:
        if not self._session_factory or not isinstance(
            self._session_factory, async_scoped_session
        ):
            raise NotFoundSessionFactoryErrorException
        return self._session_factory

    @property
    def mappers(self) -> list[Type[DeclarativeMeta]]:
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
        logger.info("Database is ready")

    async def disconnect(self) -> None:
        for engine in self._engines:
            await engine.dispose()
        logger.info("Database is disconnected")

    async def get_connection_list(self) -> list[AsyncConnection]:
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
        engine_list: list[SyncEngine | None],
        session_factory: scoped_session,
        mapper_list: list[Type[DeclarativeMeta]],
    ):
        self._engines: list[SyncEngine | None] = engine_list
        self._session_factory: scoped_session | None = session_factory
        self._mappers: list[Type[DeclarativeMeta]] = mapper_list

    @property
    def engines(self) -> list[SyncEngine | None]:
        if not self._engines:
            raise NotFoundEngineErrorException
        return self._engines

    @property
    def session_factory(self) -> scoped_session | None:
        if not self._session_factory or not isinstance(
            self._session_factory, scoped_session
        ):
            raise NotFoundSessionFactoryErrorException
        return self._session_factory

    @property
    def mappers(self) -> list[Type[DeclarativeMeta]]:
        if not self._mappers:
            raise NotFoundMapperErrorException
        return self._mappers

    def create_all(self) -> None:
        if not self._engines:
            raise NotFoundEngineErrorException
        if not self._mappers:
            raise NotFoundMapperErrorException

        for engine, mapper in zip(self._engines, self._mappers):
            with engine.begin():
                mapper.metadata.create_all(engine)

    def get_connection_list(self) -> list[SyncConnection]:
        connection_list = list()
        for engine in self._engines:
            connection_list.append(engine.connect())
        return connection_list

    def get_transaction_list(self) -> list[Transaction]:
        transaction_list = list()
        for engine in self._engines:
            transaction_list.append(engine.connect().get_transaction())
        return transaction_list

    def disconnect(self) -> None:
        for engine in self._engines:
            engine.dispose()

    @contextmanager
    def session(self) -> Callable[..., ContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
