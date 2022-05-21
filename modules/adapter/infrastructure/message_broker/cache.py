from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any


class Cache(ABC):
    @abstractmethod
    def scan(self, pattern: str) -> None:
        pass

    @abstractmethod
    def get_after_scan(self) -> dict | None:
        pass

    @abstractmethod
    def set(
        self,
        key: Any,
        value: Any,
        ex: int | timedelta | None = None,
    ) -> None:
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        pass

    @abstractmethod
    def get_by_key(self, key: str) -> str:
        pass

    @abstractmethod
    def flushall(self) -> None:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass