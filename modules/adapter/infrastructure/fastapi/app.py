from fastapi import FastAPI

from modules.adapter.infrastructure.fastapi.config import fastapi_config
from modules.adapter.infrastructure.fastapi.middleware import init_middleware
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.presentation.api.controller import init_routers

logger = logger_.getLogger(__name__)


def create_app() -> FastAPI:
    fastapi: FastAPI = FastAPI(
        debug=fastapi_config.DEBUG,
        app_host=fastapi_config.APP_HOST,
        app_port=fastapi_config.APP_PORT,
        reload=fastapi_config.RELOAD,
    )

    init_middleware(app=fastapi)
    init_routers(app=fastapi)

    print(f"\n💌💌💌FastAPI Config is {fastapi_config.ENV}")

    return fastapi


app = create_app()


@app.on_event("startup")
async def init_infrastructure():
    db.create_all()


@app.on_event("shutdown")
async def tear_down_db():
    db.disconnect()
