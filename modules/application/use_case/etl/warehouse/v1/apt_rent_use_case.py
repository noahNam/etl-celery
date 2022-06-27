from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealsRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)

from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptRentsJoinKeyEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import (
    AptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_rent_model import (
    GovtAptRentModel,
)
from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class AptRentUseCase(BaseETLUseCase):
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
        govt_apt_rents: list[
            GovtAptRentsJoinKeyEntity
        ] = self._govt_deal_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.APT_RENTS_INPUT.value
        )
        if not govt_apt_rents:
            print("govt_apt_rents 업데이트 필요한 데이터 없음")
            return

        house_ids = list()
        for govt_apt_rent in govt_apt_rents:
            house_ids.append(govt_apt_rent.house_id)

        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_house_ids(house_ids=house_ids)

        # Transfer
        results: tuple[list[AptRentModel], list[int]] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.APT_RENTS_INPUT.value,
            entities=govt_apt_rents,
            supply_areas=supply_areas,
        )
        apt_rents: list[AptRentModel] = results[0]
        govt_apt_rent_ids: list[int] = results[1]

        # Load
        self._bld_deal_reop.save_all(
            insert_models=apt_rents,
            ids=govt_apt_rent_ids,
            update_model=GovtAptRentModel,
        )
