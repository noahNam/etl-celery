from http import HTTPStatus
from fastapi import HTTPException


class InvalidRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


class InvalidConfigErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="invalid config setting parameters")


class NotFoundEngineErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="database_engine_connection_error")


class NotFoundMapperErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="database_mapper_check_error")


class NotFoundSessionFactoryErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="session_factory_check_error")


class SqlAlchemyMiddlewareErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="session_roll_backed_during_call_next_error")


class ValueObjectValidationException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="value_object_validation_failed")


class EntityValidationException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="entity_object_validation_failed")


class SessionErrorException(InternalServerErrorException):
    def __init__(self):
        super().__init__(detail="session_roll_backed_during_call_next_error")


class NotUniqueErrorException(InvalidRequestException):
    def __init__(self):
        super().__init__(detail="not_unique_error")
