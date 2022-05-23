from typing import Callable, AsyncContextManager, ContextManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class BaseAsyncRepository:
    def __init__(
        self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]
    ) -> None:
        self._session_factory = session_factory

    @property
    def session_factory(self) -> Callable[..., AsyncContextManager[AsyncSession]]:
        return self._session_factory


class BaseSyncRepository:
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self._session_factory = session_factory

    @property
    def session_factory(self) -> Callable[..., ContextManager[Session]]:
        return self._session_factory
