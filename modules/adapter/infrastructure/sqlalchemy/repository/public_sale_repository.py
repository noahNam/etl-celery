from sqlalchemy import select

from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datamart.v1.public_sale_entity import (
    PublicDtUniqueEntity,
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
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncPublicSaleRepository:
    def save_all(
        self, models: list[PublicSaleModel] | list[PublicSaleDetailModel]
    ) -> None:
        if not models:
            return None

        try:
            session.add_all(models)
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

    def save_all_update_needed(
        self, special_supply_results: list[SpecialSupplyResultModel], sub_ids: list[int]
    ) -> None:
        if not special_supply_results:
            return None

        try:
            session.add_all(special_supply_results)
            session.commit()
        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][{type(special_supply_results[0])}]"
                f" updated_at : {special_supply_results[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception
