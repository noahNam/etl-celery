from fastapi import FastAPI

from modules.adapter.infrastructure.fastapi.middleware.authentication import (
    AuthenticationMiddleware,
)
from modules.adapter.infrastructure.fastapi.middleware.sqlalchemy import (
    SQLAlchemyMiddleware,
)


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(SQLAlchemyMiddleware)
    app.add_middleware(AuthenticationMiddleware)
