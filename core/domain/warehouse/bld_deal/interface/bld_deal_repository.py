from abc import ABC, abstractmethod
from typing import Type

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import (
    AptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import (
    AptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import (
    OfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import (
    OfctlRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import (
    RightLotOutModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_rent_model import (
    GovtAptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_deal_model import (
    GovtOfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_rent_model import (
    GovtOfctlRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_right_lot_out_model import (
    GovtRightLotOutModel,
)


class BldDealRepository(ABC):
    @abstractmethod
    def save_all(
        self,
        models: list[AptDealModel]
        | list[AptRentModel]
        | list[OfctlDealModel]
        | list[OfctlRentModel]
        | list[RightLotOutModel],
        ids: list[int],
        update_model: Type[
            GovtAptDealModel
            | GovtAptRentModel
            | GovtOfctlDealModel
            | GovtOfctlRentModel
            | GovtRightLotOutModel
        ],
    ) -> None:
        pass
