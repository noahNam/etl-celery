from http import HTTPStatus

import jwt
from fastapi.responses import ORJSONResponse
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from exceptions.authentication import (
    InvalidTokenPrefixException,
    AuthorizationException,
)
from modules.adapter.infrastructure.fastapi.config import fastapi_config


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        prefix: str = "Bearer"
        authorization: str | None = request.headers.get("Authorization")

        try:
            if not authorization:
                raise AuthorizationException

            bearer, _, token = authorization.partition(" ")

            # 'Bearer' 로 시작하지 않을 경우
            if bearer != prefix:
                raise InvalidTokenPrefixException

            jwt.decode(
                jwt=token,
                key=fastapi_config.JWT_SECRET_KEY,
                algorithms=[fastapi_config.JWT_ALGORITHM],
            )
            response = await call_next(request)
        except InvalidTokenError:
            return ORJSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"detail": "Invalid Token Error"},
            )
        except AuthorizationException:
            return ORJSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={"detail": "Not found Authorization from Header"},
            )
        except InvalidTokenPrefixException:
            return ORJSONResponse(
                status_code=HTTPStatus.BAD_REQUEST, content={"detail": "Invalid Prefix"}
            )

        return response
