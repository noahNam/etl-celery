from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)


class KaptRepository(ABC):
    @abstractmethod
    async def find_by_id(self, house_id: int) -> KaptOpenApiInputEntity | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[KaptOpenApiInputEntity]:
        pass

    @abstractmethod
    async def save(
        self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None
    ) -> None:
        pass
