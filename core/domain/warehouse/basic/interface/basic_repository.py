from abc import ABC, abstractmethod
from typing import Type

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import BasicInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import DongInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import MgmtCostModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.type_info_model import TypeInfoModel


class BasicRepository(ABC):
    @abstractmethod
    def save(self, target_model: Type[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel], values: list[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel]) -> None:
        pass
