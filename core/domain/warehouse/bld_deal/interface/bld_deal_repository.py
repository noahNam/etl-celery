from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import OfctlDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import OfctlRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel


class BldDealRepository(ABC):
    @abstractmethod
    def save_all(self, models: list[AptDealModel] | list[AptRentModel] | list[OfctlDealModel] | list[OfctlRentModel] | list[RightLotOutModel]) -> None:
        pass