from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from http import HTTPStatus
from uuid import uuid4

from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import session_factory
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if not session_factory:
            logger.error(
                f"[SqlAlchemyMiddleware][dispatch] error : session_factory is {session_factory}"
            )
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"detail": "not found session_factory"},
            )

        session_id = str(uuid4())
        SessionContextManager.set_context_value(value=session_id)

        try:
            response = await call_next(request)

        except Exception as e:
            await session_factory.rollback()
            logger.error(f"[SqlAlchemyMiddleware][dispatch] error : {e}")
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"detail": f"session_roll_backed_during_call_next_error - {e}"},
            )
        finally:
            # Sync_DB 사용시 await 제거 후 사용
            await session_factory.remove()
        return response
