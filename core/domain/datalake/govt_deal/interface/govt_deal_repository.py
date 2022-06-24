from abc import ABC, abstractmethod


class GovtDealsRepository(ABC):
    @abstractmethod
    def find_by_update_needed(self, model) -> None:
        pass