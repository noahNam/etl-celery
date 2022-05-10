import os
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from uvloop import new_event_loop

from modules.adapter.infrastructure.fastapi.app import create_app
from modules.adapter.infrastructure.fastapi.config import TestConfig
from modules.adapter.infrastructure.sqlalchemy.connection import AsyncDatabase
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import get_db_config


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
    config.USE_ASYNC_DB = True
    return config.dict()


@pytest.fixture(scope="session")
def sync_config() -> dict:
    config: TestConfig = TestConfig()
    config.USE_ASYNC_DB = False
    config.DB_URL = "sqlite:///:memory:"
    return config.dict()


@pytest.fixture(scope="session")
async def async_db(async_config):
    test_engine = create_async_engine(**get_db_config(async_config))
    test_session_factory = async_scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=test_engine,
            class_=AsyncSession,
        ),
        scopefunc=SessionContextManager.get_context,
    )
    db = AsyncDatabase(engine=test_engine, session_factory=test_session_factory)

    yield db

    # tear_down
    await db.disconnect()


@pytest_asyncio.fixture
async def async_session(async_db, async_config) -> AsyncGenerator:
    mapper = async_db.mapper
    # Start Connection
    connection = await async_db.get_connection()

    if is_sqlite_used(async_config.get("DB_URL")):
        await connection.run_sync(mapper.metadata.drop_all)
        await connection.run_sync(mapper.metadata.create_all)

    try:
        # session context manager 시작
        yield async_db.session
    except Exception as e:
        await async_db.session_factory.rollback()
        print(f"session rollback due to error: {e}")

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
