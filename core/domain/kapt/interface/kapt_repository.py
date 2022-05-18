from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)


class KaptRepository(ABC):
    @abstractmethod
    async def find_by_id(self, house_id: int) -> KaptOpenApiInputEntity | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[KaptOpenApiInputEntity]:
        pass

    # @abstractmethod
    # async def save(self, kapt: Kapt) -> Kapt:
    #     pass
