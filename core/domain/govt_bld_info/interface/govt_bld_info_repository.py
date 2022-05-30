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


class GovtHouseDealRepository(ABC):
    @abstractmethod
    def save(
        self, model: GovtBldTopInfoModel | GovtBldMiddleInfoModel | GovtBldAreaInfoModel
    ) -> None:
        pass
