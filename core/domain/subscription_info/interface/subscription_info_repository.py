from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)


class SubscriptionInfoRepository(ABC):
    @abstractmethod
    def save(self, model: SubscriptionInfoModel | SubscriptionManualInfoModel) -> None:
        pass
