from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession


class BaseAsyncRepository:
    def __init__(
        self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]
    ) -> None:
        self._session_factory = session_factory

    @property
    def session_factory(self) -> Callable[..., AsyncContextManager[AsyncSession]]:
        return self._session_factory
