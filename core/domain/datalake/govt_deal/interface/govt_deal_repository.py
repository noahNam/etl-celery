from abc import ABC, abstractmethod


class GovtDealsRepository(ABC):
    @abstractmethod
    def save(self, model) -> None:
        pass

    @abstractmethod
    def find_by_id(self, pk: int): #  fixme: id로 변경시 이미 있는 내장변수로 나옴
        pass