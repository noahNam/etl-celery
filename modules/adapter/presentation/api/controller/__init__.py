from fastapi import FastAPI, APIRouter

from modules.adapter.presentation.api.controller.main import main_router

api_router = APIRouter()

api_router.include_router(main_router)


def init_routers(app: FastAPI) -> None:
    app.include_router(api_router)
