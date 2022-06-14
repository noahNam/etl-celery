from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
)


class GovtAptDealsRepository(ABC):
    @abstractmethod
    def save(self, model: GovtAptDealModel) -> None:
        pass

    @abstractmethod
    def find_by_id(self, house_id: int) -> GovtAptDealsEntity | None:
        pass