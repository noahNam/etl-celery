from contextvars import ContextVar, Token
from typing import Any

session_context: ContextVar[str] = ContextVar("session_context")


class SessionContextManager:
    _context: ContextVar[str] = session_context

    @classmethod
    def get_context(cls) -> Any:
        return cls._context.get()

    @classmethod
    def set_context_value(cls, value: str) -> Token:
        return cls._context.set(value)

    @classmethod
    def reset_context(cls, context: Token) -> None:
        cls._context.reset(context)
