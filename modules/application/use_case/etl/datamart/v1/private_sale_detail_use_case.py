import os

from modules.adapter.infrastructure.etl.mart_private_sale_details import TransformPrivateSaleDetail
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import AptDealEntity, AptRentEntity, \
    OfctlDealEntity, OfctlRentEntity, RightLotOutEntity
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import CodeRuleKeyEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_detail_model import \
    PrivateSaleDetailModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import OfctlDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import OfctlRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import SyncBldDealRepository
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import SyncKaptRepository
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BasePrivateSaleDetailUseCase:
    def __init__(
        self,
        topic: str,
        bld_deal_repo: SyncBldDealRepository,
        private_sale_repo: SyncPrivateSaleRepository,
        kapt_repo: SyncKaptRepository,
    ):
        self._topic: str = topic
        self._bld_deal_repo: SyncBldDealRepository = bld_deal_repo
        self._private_sale_repo: SyncPrivateSaleRepository = private_sale_repo
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._transfer: TransformPrivateSaleDetail = TransformPrivateSaleDetail()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class PrivateSaleDetailUseCase(BasePrivateSaleDetailUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        results = list()
        # 아파트 실거래가 정보
        apt_deals: list[AptDealEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=AptDealModel
        )
        apt_deal_results: list[PrivateSaleDetailModel] | None = self._transfer.start_etl(
            target_list=apt_deals
        )
        if apt_deal_results:
            results.extend(apt_deal_results)

        # 아파트 전월세
        apt_rents: list[AptRentEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=AptRentModel
        )
        apt_rent_results: list[PrivateSaleDetailModel] | None = self._transfer.start_etl(
            target_list=apt_rents
        )
        if apt_rent_results:
            results.extend(apt_rent_results)

        # 오피스텔 실거래가
        ofctl_deals: list[OfctlDealEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=OfctlDealModel
        )
        ofctl_deal_results: list[PrivateSaleDetailModel] | None = self._transfer.start_etl(
            target_list=ofctl_deals
        )
        if ofctl_deal_results:
            results.extend(ofctl_deal_results)

        # 오피스텔 전월세
        ofctl_rents: list[OfctlRentEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=OfctlRentModel
        )
        ofctl_rent_results: list[PrivateSaleDetailModel] | None = self._transfer.start_etl(
            target_list=ofctl_rents
        )
        if ofctl_rent_results:
            results.extend(ofctl_rent_results)

        # 분양권 전매
        right_to_outs: list[RightLotOutEntity] | None = self._bld_deal_repo.find_to_update(
            target_model=RightLotOutModel
        )
        right_to_out_results: list[PrivateSaleDetailModel] | None = self._transfer.start_etl(
            target_list=right_to_outs
        )
        if right_to_out_results:
            results.extend(right_to_out_results)

        if results:
            self.__upsert_to_datamart(results=results)

    """
    insert, update
    """

    def __upsert_to_datamart(
        self,
        results: list[PrivateSaleDetailModel],
    ) -> None:

        last_seq = None
        for result in results:
            exists_result: bool = self._private_sale_repo.exists_by_key(value=result)

            if not exists_result:
                # get last_id by code_rules
                last_seq= self._kapt_repo.find_id_by_code_rules(key_div=CodeRuleKeyEnum.PRIVATE_SALE_DETAIL_ID.value)
                result.id = last_seq

                # insert
                self._private_sale_repo.save(value=result)
            else:
                # update
                self._private_sale_repo.update(value=result)

            # self._bld_deal_repo.change_update_needed_status(value=result)

        if last_seq:
            self._kapt_repo.update_id_to_code_rules(key_div=CodeRuleKeyEnum.PRIVATE_SALE_DETAIL_ID.value, last_id=last_seq)

