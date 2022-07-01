from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsJoinKeyEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import (
    AptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealRepository,
)
from modules.application.use_case.etl import BaseETLUseCase


class AptDealUseCase(BaseETLUseCase):
    def __init__(
        self,
        govt_deal_repo,
        bld_mapping_repo,
        bld_deal_repo,
        basic_repo,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._bld_mapping_repo = bld_mapping_repo
        self._govt_deal_repo: SyncGovtDealRepository = govt_deal_repo  # input_table
        self._bld_deal_reop: SyncBldDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()
        self._basic_repo: SyncBasicRepository = basic_repo

    def execute(self):
        # Extract
        govt_apt_deals: list[
            GovtAptDealsJoinKeyEntity
        ] = self._govt_deal_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.APT_DEALS_INPUT.value
        )
        if not govt_apt_deals:
            print("govt_apt_deals 업데이트 필요한 데이터 없음")
            return

        house_ids = list()
        for govt_apt_rent in govt_apt_deals:
            house_ids.append(govt_apt_rent.house_id)

        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_house_ids(house_ids=house_ids)

        # Transfer
        results: tuple[list[AptDealModel], list[int]] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.APT_DEALS_INPUT.value,
            entities=govt_apt_deals,
            supply_areas=supply_areas,
        )
        apt_daels: list[AptDealModel] = results[0]
        govt_apt_deals: list[int] = results[1]

        # Load
        self._bld_deal_reop.save_all(
            insert_models=apt_daels, ids=govt_apt_deals, update_model=GovtAptDealModel
        )
