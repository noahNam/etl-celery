from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)


class SubscriptionRepository(ABC):
    @abstractmethod
    def save(self, value: SubscriptionModel | SubscriptionDetailModel) -> None:
        pass
