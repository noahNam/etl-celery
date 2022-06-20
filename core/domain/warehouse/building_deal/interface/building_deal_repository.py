from abc import ABC, abstractmethod


class BuildingDealsRepository(ABC):
    @abstractmethod
    def save(self, model) -> None:
        pass

    @abstractmethod
    def find_by_id(self, pk: int):
        pass