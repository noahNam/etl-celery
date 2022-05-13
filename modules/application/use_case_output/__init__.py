class UseCaseFailureOutput:
    def __init__(
        self,
        type: str | int,
        code: int,
        message: str | None = None,
    ) -> None:
        self.type = type
        self.message = self._format_message(message)
        self.code = code

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return msg.__class__.__name__
        return msg

    @property
    def value(self) -> dict:
        return {"type": self.type, "message": self.message}

    def __bool__(self):
        return False


class UseCaseSuccessOutput:
    SUCCESS = "success"

    def __init__(self, value=None, meta=None):
        self._type = self.SUCCESS
        self._value = value
        self._meta = meta

    def __bool__(self):
        return True

    @property
    def value(self):
        return self._value

    @property
    def meta(self):
        return self._meta

    @property
    def type(self):
        return self._type


class FailureType:
    INVALID_REQUEST_ERROR = "invalid_request_error"
    UNAUTHORIZED_ERROR = "unauthorized_error"
    INTERNAL_ERROR = "internal_server_error"
    NOT_FOUND_ERROR = "not_found_error"
    SYSTEM_ERROR = "system_error"
    ALREADY_EXIST = "already_exist"
