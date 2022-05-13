from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

from exceptions.base import InvalidConfigErrorException
from modules.adapter.infrastructure.fastapi.config import fastapi_config
from modules.adapter.infrastructure.sqlalchemy.connection import AsyncDatabase
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager


def get_db_config(config: dict) -> dict:
    if not config.get("DB_URL"):
        raise InvalidConfigErrorException

    db_config = {
        "url": config.get("DB_URL"),
        "echo": config.get("DB_ECHO"),
        "pool_pre_ping": config.get("DB_PRE_PING"),
    }

    return db_config


"""SyncDatabase를 사용해야 하는 경우 (Alembic 등)
engine = create_engine(**get_db_config(fastapi_config.dict()))

session_factory: scoped_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=Session,
    ),
    scopefunc=SessionContextManager.get_context,
)
db: SyncDatabase = SyncDatabase(engine=engine, session_factory=session_factory)
"""
engine = create_async_engine(**get_db_config(fastapi_config.dict()))

session_factory: async_scoped_session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
    ),
    scopefunc=SessionContextManager.get_context,
)
db: AsyncDatabase = AsyncDatabase(engine=engine, session_factory=session_factory)
