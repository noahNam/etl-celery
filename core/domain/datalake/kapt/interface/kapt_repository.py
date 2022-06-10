from abc import ABC, abstractmethod
from typing import Any, Type

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptOpenApiInputEntity,
    KakaoApiInputEntity, KaptBasicInfoEntity, KaptAreaInfoEntity, KaptLocationInfoEntity, KaptMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import \
    KaptBasicInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_mgmt_cost_model import KaptMgmtCostModel


class KaptRepository(ABC):
    @abstractmethod
    def find_by_id(
            self, house_id: int, find_type: int
    ) -> KaptOpenApiInputEntity | KakaoApiInputEntity | None:
        pass

    @abstractmethod
    def find_all(
            self, find_type: int
    ) -> list[KaptOpenApiInputEntity] | list[KakaoApiInputEntity]:
        pass

    @abstractmethod
    def save(self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None) -> None:
        pass

    @abstractmethod
    def find_by_date(
            self, target_model: Type[KaptBasicInfoModel | KaptAreaInfoModel | KaptLocationInfoModel | KaptMgmtCostModel], date: str
    ) -> list[KaptBasicInfoEntity | KaptAreaInfoEntity | KaptLocationInfoEntity | KaptMgmtCostEntity] | None:
        pass
