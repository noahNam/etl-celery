from abc import ABC, abstractmethod

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


class GovtHouseDealRepository(ABC):
    @abstractmethod
    def save(
        self,
        model: GovtAptDealModel
        | GovtAptRentModel
        | GovtOfctlDealModel
        | GovtOfctlRentModel
        | GovtRightLotOutModel,
    ) -> None:
        pass
