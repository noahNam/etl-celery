from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.public_sale_repository import (
    SyncPublicSaleRepository
)

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity,
    SubDtToPublicDtEntity
)
from modules.adapter.infrastructure.etl.mart_public_sales import TransformPublicSales
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)

class PublicSalesUseCase():
    def __init__(self, subscription_repo, public_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._transfer: TransformPublicSales = TransformPublicSales()
        self.public_repo: SyncPublicSaleRepository = public_repo

    def execute(self):
        # public_sales
        subscriptions: list[SubsToPublicEntity] = self._subscription_repo.find_by_update_needed(
            model=SubscriptionModel
        )
        if not subscriptions:
            logger.info(
                "[PublicSalesUseCase] There is nothing to update in subscriptions"
            )
        else:
            public_sales: list[PublicSaleModel] = self._transfer.start_transfer_public_sales(
                subscriptions=subscriptions
            )
            self.public_repo.save_all(public_sales)

        # public_sale_details
        sub_details: list[SubDtToPublicDtEntity] = self._subscription_repo.find_by_update_needed(
            model=PublicSaleDetailModel
        )
        if not subscriptions:
            logger.info(
                "[PublicSalesUseCase] There is nothing to update in subscription_details"
            )
        else:
            public_sale_details: list[PublicSaleDetailModel] = self._transfer.start_transfer_public_sale_details(
                sub_details=sub_details
            )
            self.public_repo.save_all(public_sale_details)
