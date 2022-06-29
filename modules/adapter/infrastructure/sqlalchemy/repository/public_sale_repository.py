from sqlalchemy import select, update

from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datamart.v1.public_sale_entity import (
    PublicDtUniqueEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity,
    SubDtToPublicDtEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.special_supply_result_model import (
    SpecialSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.general_supply_result_model import (
    GeneralSupplyResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)

from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncPublicSaleRepository:
    def save_all(
            self,
            models: list[PublicSaleModel],
            sub_ids: list[int]
    ) -> None:
        if not models:
            return None

        try:
            session.add_all(models)
            session.execute(
                update(SubscriptionModel)
                    .where(SubscriptionModel.subs_id.in_(sub_ids))
                    .values(update_needed=False)
            )
            session.commit()

        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all][{type(models[0])}] updated_at : {models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception

    def find_to_detail_ids_by_sub_ids(
        self, sub_ids: list[int]
    ) -> list[PublicDtUniqueEntity]:
        query = select(PublicSaleDetailModel).where(
            PublicSaleDetailModel.public_sale_id.in_(sub_ids)
        )
        results = session.execute(query).scalars().all()
        return [result.to_unique_entity() for result in results]

    def save_all_details(
            self,
            public_sale_details: list[PublicSaleDetailModel],
            special_supply_results: list[SpecialSupplyResultModel],
            general_supply_results: list[GeneralSupplyResultModel],
            sub_detail_ids: list[int]
    ) -> None:
        if not public_sale_details:
            return None

        try:
            session.add_all(public_sale_details)
            session.add_all(special_supply_results)
            session.add_all(general_supply_results)
            session.execute(
                update(SubscriptionDetailModel)
                    .where(SubscriptionDetailModel.id.in_(sub_detail_ids))
                    .values(update_needed=False)
            )
            session.commit()
        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][{type(special_supply_results[0])}]"
                f" updated_at : {special_supply_results[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception
