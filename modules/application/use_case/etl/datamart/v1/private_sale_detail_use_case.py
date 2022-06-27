import json

from modules.adapter.infrastructure.etl.mart_private_sale_details import (
    TransformPrivateSaleDetail,
)
from modules.adapter.infrastructure.message.broker.redis import RedisClient
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import (
    AptDealEntity,
    AptRentEntity,
    OfctlDealEntity,
    OfctlRentEntity,
    RightLotOutEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import CodeRuleKeyEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_detail_model import (
    PrivateSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import (
    AptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import (
    AptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import (
    OfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import (
    OfctlRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import (
    RightLotOutModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase

logger = logger_.getLogger(__name__)


class PrivateSaleDetailUseCase(BaseETLUseCase):
    def __init__(
            self,
            bld_deal_repo: SyncBldDealRepository,
            private_sale_repo: SyncPrivateSaleRepository,
            kapt_repo: SyncKaptRepository,
            redis: RedisClient,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bld_deal_repo: SyncBldDealRepository = bld_deal_repo
        self._private_sale_repo: SyncPrivateSaleRepository = private_sale_repo
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._transfer: TransformPrivateSaleDetail = TransformPrivateSaleDetail()
        self._redis: RedisClient = redis


    def execute(self):
        # 아파트 실거래가 정보
        apt_deals: list[AptDealEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=AptDealModel
        )
        apt_deal_results: list[
            PrivateSaleDetailModel
        ] | None = self._transfer.start_etl(target_list=apt_deals)
        if apt_deal_results:
            self.__upsert_to_datamart(
                results=apt_deal_results, update_needed_target_entities=apt_deals
            )

        # 아파트 전월세
        apt_rents: list[AptRentEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=AptRentModel
        )
        apt_rent_results: list[
            PrivateSaleDetailModel
        ] | None = self._transfer.start_etl(target_list=apt_rents)
        if apt_rent_results:
            self.__upsert_to_datamart(
                results=apt_rent_results, update_needed_target_entities=apt_rents
            )

        # 오피스텔 실거래가
        ofctl_deals: list[OfctlDealEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=OfctlDealModel
        )
        ofctl_deal_results: list[
            PrivateSaleDetailModel
        ] | None = self._transfer.start_etl(target_list=ofctl_deals)
        if ofctl_deal_results:
            self.__upsert_to_datamart(
                results=ofctl_deal_results, update_needed_target_entities=ofctl_deals
            )

        # 오피스텔 전월세
        ofctl_rents: list[OfctlRentEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=OfctlRentModel
        )
        ofctl_rent_results: list[
            PrivateSaleDetailModel
        ] | None = self._transfer.start_etl(target_list=ofctl_rents)
        if ofctl_rent_results:
            self.__upsert_to_datamart(
                results=ofctl_rent_results, update_needed_target_entities=ofctl_rents
            )

        # 분양권 전매
        right_to_outs: list[
            RightLotOutEntity
        ] | None = self._bld_deal_repo.find_to_update(target_model=RightLotOutModel)
        right_to_out_results: list[
            PrivateSaleDetailModel
        ] | None = self._transfer.start_etl(target_list=right_to_outs)
        if right_to_out_results:
            self.__upsert_to_datamart(
                results=right_to_out_results,
                update_needed_target_entities=right_to_outs,
            )

    """
    insert, update
    """

    def __upsert_to_datamart(
        self,
        results: list[PrivateSaleDetailModel],
        update_needed_target_entities: list[
            AptDealEntity
            | AptRentEntity
            | OfctlDealEntity
            | OfctlRentEntity
            | RightLotOutEntity
        ],
    ) -> None:

        update_needed_target_ids = [
            update_needed_target_entity.id
            for update_needed_target_entity in update_needed_target_entities
        ]
        last_seq = self._kapt_repo.find_id_by_code_rules(
            key_div=CodeRuleKeyEnum.PRIVATE_SALE_DETAIL_ID.value
        )
        for idx, result in enumerate(results):
            exists_result: bool = self._private_sale_repo.exists_by_key(value=result)

            try:
                if not exists_result:
                    # get last_id by code_rules
                    last_seq += 1
                    result.id = last_seq

                    # insert
                    self._private_sale_repo.save(value=result)
                    key_div = "I"
                else:
                    # update
                    self._private_sale_repo.update(value=result)
                    key_div = "U"

                self._bld_deal_repo.change_update_needed_status(
                    target_model=update_needed_target_entities[0],
                    update_needed_id=update_needed_target_ids[idx],
                )

                # message publish to redis
                self._redis.set(
                    key=f"sync:{key_div}:private_sale_details:{result.id}",
                    value=json.dumps(result.to_dict(), ensure_ascii=False).encode(
                        "utf-8"
                    ),
                )
                self._private_sale_repo.change_update_needed_status(value=result)

            except Exception as e:
                logger.error(f"☠️\tPrivateSaleDetailUseCase - Failure! {result.id}:{e}")

                last_seq -= 1
                self._save_crawling_failure(
                    failure_value=result,
                    ref_table="private_sale_details",
                    param=result,
                    reason=e,
                )

        if last_seq:
            self._kapt_repo.update_id_to_code_rules(
                key_div=CodeRuleKeyEnum.PRIVATE_SALE_DETAIL_ID.value, last_id=last_seq
            )
