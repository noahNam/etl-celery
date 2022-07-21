import json
from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.public_sale_repository import (
    SyncPublicSaleRepository,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity,
    SubDtToPublicDtEntity,
)
from modules.adapter.infrastructure.etl.mart_public_sales import TransformPublicSales
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.special_supply_result_model import (
    SpecialSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.general_supply_result_model import (
    GeneralSupplyResultModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.message.broker.redis import RedisClient

logger = logger_.getLogger(__name__)


class PublicSaleUseCase(BaseETLUseCase):
    def __init__(
        self,
        subscription_repo: SyncSubscriptionRepository,
        public_repo: SyncPublicSaleRepository,
        redis: RedisClient,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._transfer: TransformPublicSales = TransformPublicSales()
        self.public_repo: SyncPublicSaleRepository = public_repo
        self._redis: RedisClient = redis

    def execute(self):
        subscriptions: list[
            SubsToPublicEntity
        ] = self._subscription_repo.find_by_update_needed(model=SubscriptionModel)

        if not subscriptions:
            logger.info(
                "[PublicSalesUseCase] There is nothing to update in subscriptions"
            )
            public_sales = list()
            sub_ids = list()
        else:
            public_sales: list[
                PublicSaleModel
            ] = self._transfer.start_transfer_public_sales(subscriptions=subscriptions)
            sub_ids: list[int] = self._transfer._get_sub_ids(sub_details=subscriptions)

        # extract subscription_details
        sub_details: list[
            SubDtToPublicDtEntity
        ] = self._subscription_repo.find_by_update_needed(model=SubscriptionDetailModel)
        if not subscriptions:
            logger.info(
                "[PublicSalesUseCase] There is nothing to update in subscription_details"
            )
        else:
            public_sale_details: list[
                PublicSaleDetailModel
            ] = self._transfer.start_transfer_public_sale_details(
                sub_details=sub_details
            )
            special_supply_results: list[
                SpecialSupplyResultModel
            ] = self._transfer.start_transfer_special_supply_results(
                sub_details=sub_details
            )
            general_supply_results: list[
                GeneralSupplyResultModel
            ] = self._transfer.start_transfer_general_supply_results(
                sub_details=sub_details
            )

            sub_detail_ids: list[int] = self._transfer.get_ids(sub_details=sub_details)
            self.public_repo.save_public_sales(
                public_sales=public_sales,
                sub_ids=sub_ids,
                public_sale_details=public_sale_details,
                special_supply_results=special_supply_results,
                general_supply_results=general_supply_results,
                sub_detail_ids=sub_detail_ids,
            )

            # for public_sale in public_sales:
            #     self.redis_set(model=public_sale)
            # for public_sale_detail in public_sale_details:
            #     self.redis_set(model=public_sale_detail)
            # for special_supply_result in special_supply_results:
            #     self.redis_set(model=special_supply_result)
            # for general_supply_result in general_supply_results:
            #     self.redis_set(model=general_supply_result)

    def redis_set(
        self,
        model: PublicSaleModel
        | PublicSaleDetailModel
        | SpecialSupplyResultModel
        | GeneralSupplyResultModel,
    ) -> None:
        # message publish to redis
        if isinstance(model, PublicSaleModel):
            ref_table = "public_sales"
        elif isinstance(model, PublicSaleDetailModel):
            ref_table = "public_sale_details"
        elif isinstance(model, SpecialSupplyResultModel):
            ref_table = "special_supply_results"
        elif isinstance(model, GeneralSupplyResultModel):
            ref_table = "general_supply_results"
        else:
            return None

        self._redis.set(
            key=f"sync:{ref_table}:{model.id}",
            value=json.dumps(model.to_dict(), ensure_ascii=False).encode("utf-8"),
        )
