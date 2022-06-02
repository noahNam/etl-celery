from sqlalchemy.future import Engine as SyncEngine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from exceptions.base import InvalidConfigErrorException
from modules.adapter.infrastructure.fastapi.config import fastapi_config
from modules.adapter.infrastructure.sqlalchemy.connection import SyncDatabase
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.mapper import (
    datalake_base,
    warehouse_base,
    datamart_base,
)


def get_db_config(config: dict) -> dict:
    """SQLAlchemy 관련 parameter가 더 추가되는 경우 아래 db_config에 추가하여 사용"""
    if (
        not config.get("DATA_WAREHOUSE_URL")
        or not config.get("DATA_LAKE_URL")
        or not config.get("DATA_MART_URL")
    ):
        raise InvalidConfigErrorException

    db_config = {
        "echo": config.get("DB_ECHO"),
        "pool_pre_ping": config.get("DB_PRE_PING"),
    }

    return db_config


"""AsyncDatabase를 사용해야 하는 경우
datalake_engine: AsyncEngine = create_async_engine(
    url=fastapi_config.DATA_LAKE_URL, **get_db_config(fastapi_config.dict())
)
warehouse_engine: AsyncEngine = create_async_engine(
    url=fastapi_config.DATA_WAREHOUSE_URL, **get_db_config(fastapi_config.dict())
)
datamart_engine: AsyncEngine = create_async_engine(
    url=fastapi_config.DATA_MART_URL, **get_db_config(fastapi_config.dict())
)

session_factory: async_scoped_session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        binds={datalake_base: datalake_engine, warehouse_base: warehouse_engine, datamart_base: datamart_engine},
        class_=AsyncSession,
    ),
    scopefunc=SessionContextManager.get_context,
)
db: AsyncDatabase = AsyncDatabase(
    engine_list=[datalake_engine, warehouse_engine, datamart_engine],
    session_factory=session_factory,
    mapper_list=[datalake_base, warehouse_base, datamart_base],
)

"""

datalake_engine: SyncEngine = create_engine(
    url=fastapi_config.DATA_LAKE_URL,
    future=True,
    **get_db_config(fastapi_config.dict())
)
warehouse_engine: SyncEngine = create_engine(
    url=fastapi_config.DATA_WAREHOUSE_URL,
    future=True,
    **get_db_config(fastapi_config.dict())
)
datamart_engine: SyncEngine = create_engine(
    url=fastapi_config.DATA_MART_URL,
    future=True,
    **get_db_config(fastapi_config.dict())
)

session_factory: scoped_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        binds={
            datalake_base: datalake_engine,
            warehouse_base: warehouse_engine,
            datamart_base: datamart_engine,
        },
        class_=Session,
        future=True,
    ),
    scopefunc=SessionContextManager.get_context,
)
db: SyncDatabase = SyncDatabase(
    engine_list=[datalake_engine, warehouse_engine, datamart_engine],
    session_factory=session_factory,
    mapper_list=[datalake_base, warehouse_base, datamart_base],
)
