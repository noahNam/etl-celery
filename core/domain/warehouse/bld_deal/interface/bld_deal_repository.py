from abc import ABC, abstractmethod


class BldDealsRepository(ABC):
    @abstractmethod
    def save_all(self, models) -> None:
        pass
