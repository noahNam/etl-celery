from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_area_info_model import (
    GovtBldAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_middle_info_model import (
    GovtBldMiddleInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_top_info_model import (
    GovtBldTopInfoModel,
)


class GovtBldRepository(ABC):
    @abstractmethod
    def save(
        self,
        bld_orm: GovtBldTopInfoModel | GovtBldMiddleInfoModel | GovtBldAreaInfoModel,
    ) -> None:
        pass

    @abstractmethod
    def is_exists(
        self,
        bld_orm: GovtBldTopInfoModel | GovtBldMiddleInfoModel | GovtBldAreaInfoModel,
    ) -> bool:
        pass
