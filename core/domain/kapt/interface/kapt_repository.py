from abc import ABC, abstractmethod


class KaptRepository(ABC):
    @abstractmethod
    async def find_by_id(self, house_id: int):
        pass

    # @abstractmethod
    # async def save(self, kapt: Kapt) -> Kapt:
    #     pass
