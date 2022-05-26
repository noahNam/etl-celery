from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class CallFailureHistoryRepository(ABC):
    @abstractmethod
    def save(self, fail_orm) -> None:
        pass

    @abstractmethod
    def find_by_id(self, fail_id: int) -> Type[BaseModel] | None:
        pass
