from abc import ABC, abstractmethod
from typing import Type

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.applyhome_dl_model import (
    ApplyHomeModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.google_sheet_applyhome_dl_model import (
    GoogleSheetApplyHomeModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)


class SubscriptionRepository(ABC):
    @abstractmethod
    def save(
        self,
        target_model: Type[ApplyHomeModel | GoogleSheetApplyHomeModel],
        values: list[SubscriptionInfoModel | SubscriptionManualInfoModel],
    ) -> None:
        pass
