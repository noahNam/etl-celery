from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptOpenApiInputEntity,
    KakaoApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)


class KaptRepository(ABC):
    @abstractmethod
    def find_all(
        self, find_type: int
    ) -> list[KaptOpenApiInputEntity] | list[KakaoApiInputEntity]:
        pass

    @abstractmethod
    def save(self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None) -> None:
        pass
