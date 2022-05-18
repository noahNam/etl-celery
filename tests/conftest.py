import os
from typing import Generator, AsyncGenerator, List

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    AsyncSession,
    AsyncEngine,
    AsyncConnection,
)
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from uvloop import new_event_loop

from modules.adapter.infrastructure.fastapi.app import create_app
from modules.adapter.infrastructure.fastapi.config import TestConfig
from modules.adapter.infrastructure.sqlalchemy.connection import AsyncDatabase
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import get_db_config, db
from modules.adapter.infrastructure.sqlalchemy.mapper import (
    datalake_base,
    warehouse_base,
)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
async def running_app(app, async_config):
    async with LifespanManager(app=app):
        yield app


@pytest.fixture(scope="session")
def sync_client(app: FastAPI) -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    """pytest->event_loop fixture를 override 하기 위한 코드"""
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client(running_app) -> AsyncGenerator:
    async with AsyncClient(app=running_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def async_config() -> dict:
    config: TestConfig = TestConfig()
    return config.dict()


@pytest.fixture(scope="session")
def sync_config() -> dict:
    config: TestConfig = TestConfig()
    config.DATA_LAKE_URL = "sqlite:///:memory:"
    config.DATA_WAREHOUSE_URL = "sqlite:///:memory:"
    return config.dict()


@pytest.fixture(scope="session")
async def async_db(async_config):
    _is_local_db_used(database_url=async_config.get("DATA_LAKE_URL"))
    _is_local_db_used(database_url=async_config.get("DATA_WAREHOUSE_URL"))

    if is_sqlite_used(async_config.get("DATA_LAKE_URL")) or is_sqlite_used(
        async_config.get("DATA_WAREHOUSE_URL")
    ):

        test_datalake_engine: AsyncEngine = create_async_engine(
            url="sqlite+aiosqlite:///:memory:", **get_db_config(async_config)
        )
        test_warehouse_engine: AsyncEngine = create_async_engine(
            url="sqlite+aiosqlite:///:memory:", **get_db_config(async_config)
        )
        test_session_factory = async_scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                binds={
                    datalake_base: test_datalake_engine,
                    warehouse_base: test_warehouse_engine,
                },
                class_=AsyncSession,
            ),
            scopefunc=SessionContextManager.get_context,
        )
        _db: AsyncDatabase = AsyncDatabase(
            engine_list=[test_datalake_engine, test_warehouse_engine],
            session_factory=test_session_factory,
            mapper_list=[datalake_base, warehouse_base],
        )
    else:
        # local async db, not memory db
        _db = db

    yield _db

    # tear_down
    await _db.disconnect()


@pytest_asyncio.fixture
async def async_session(async_db) -> AsyncGenerator:
    # Start Connection
    connections: List[AsyncConnection] = await async_db.get_connection_list()

    for connection, engine, mapper in zip(
        connections, async_db.engines, async_db.mappers
    ):
        await connection.run_sync(mapper.metadata.drop_all)
        await connection.run_sync(mapper.metadata.create_all)

    try:
        # session context manager 시작
        yield async_db.session
    except Exception as e:
        await async_db.session_factory.rollback()
        print(f"session rollback due to error: {e}")

    for connection in connections:
        # tear_down connection
        await connection.rollback()
        await connection.close()


def is_sqlite_used(database_url: str):
    if ":memory:" in database_url:
        return True
    return False


def _is_local_db_used(database_url: str):
    """
    local db를 사용하면 memory db 삭제
    """
    if ":memory:" not in database_url:
        if os.path.exists(database_url.split("sqlite:///")[-1]):  # :memory:
            os.unlink(database_url.split("sqlite:///")[-1])
