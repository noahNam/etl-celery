from abc import ABC, abstractmethod
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)


class SubscriptionInfoRepository(ABC):
    @abstractmethod
    def save_to_new_schema(
        self, value: SubscriptionInfoModel | SubscriptionManualInfoModel
    ) -> None:
        pass
