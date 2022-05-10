from exceptions.base import (
    InvalidRequestException,
    UnauthorizedException,
    NotFoundException,
)


class InvalidTokenPrefixException(InvalidRequestException):
    def __init__(self):
        super().__init__(detail="Invalid Prefix")


class InvalidTokenException(UnauthorizedException):
    def __init__(self):
        super().__init__(detail="Invalid Token Error")


class AuthorizationException(NotFoundException):
    def __init__(self):
        super().__init__(detail="Not found Authorization from Header")
