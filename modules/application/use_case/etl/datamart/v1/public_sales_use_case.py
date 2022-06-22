from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.public_sale_repository import (
    PublicSaleRepository
)

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity
)
from modules.adapter.infrastructure.etl.mart_public_sales import TransformPublicSales
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)


class PublicSalesUseCase():
    def __init__(self, subscription_repo, public_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._transfer: TransformPublicSales = TransformPublicSales()
        self.public_repo: PublicSaleRepository = public_repo

    def execute(self):
        subscriptions: list[SubsToPublicEntity] = self._subscription_repo.find_by_update_needed()
        if not subscriptions:
            print("subscriptions 신규 데이터 없음")
            return None

        public_sales: list[PublicSaleModel] = self._transfer.start_transfer(subscriptions=subscriptions)

        self.public_repo.save_all(public_sales)

