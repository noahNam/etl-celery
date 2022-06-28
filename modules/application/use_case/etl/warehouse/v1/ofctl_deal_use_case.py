from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealsRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtOfctlDealJoinKeyEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import (
    OfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_deal_model import (
    GovtOfctlDealModel,
)
from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class OfctlDealUseCase(BaseETLUseCase):
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
        self._bld_mapping_repo: SyncBldMappingResultsRepository = (
            bld_mapping_repo  # input_table
        )
        self._govt_deal_repo: SyncGovtDealsRepository = govt_deal_repo  # input_table
        self._bld_deal_reop: SyncBldDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()
        self._basic_repo: SyncBasicRepository = basic_repo

    def execute(self):
        govt_ofctl_deals: list[
            GovtOfctlDealJoinKeyEntity
        ] = self._govt_deal_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.OFCTL_DEAL_INPUT.value
        )
        if not govt_ofctl_deals:
            print("govt_apt_deals 업데이트 필요한 데이터 없음")
            return

        house_ids = list()
        for govt_apt_rent in govt_ofctl_deals:
            house_ids.append(govt_apt_rent.house_id)

        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_house_ids(house_ids=house_ids)

        # Transfer
        results: tuple[list[OfctlDealModel], list[int]] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.OFCTL_DEAL_INPUT.value,
            entities=govt_ofctl_deals,
            supply_areas=supply_areas,
        )
        ofctl_deals: list[OfctlDealModel] = results[0]
        govt_ofctl_deal_ids: list[int] = results[1]

        # Load
        self._bld_deal_reop.save_all(
            insert_models=ofctl_deals,
            ids=govt_ofctl_deal_ids,
            update_model=GovtOfctlDealModel,
        )
