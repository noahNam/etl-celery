from datetime import date

from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository
)

from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealsRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.building_deal_repository import (
    SyncBuildingDealRepository
)

from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptRentsJoinKeyEntity
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class AptRentUseCase(BaseETLUseCase):
    def __init__(self, govt_deal_repo, bld_mapping_repo, bld_deal_repo, *args, **kwargs):  # fixme: 명칭 통일 및 수정
        super().__init__(*args, **kwargs)
        self._bld_mapping_repo: SyncBldMappingResultsRepository = bld_mapping_repo  # input_table
        self._govt_deal_repo: SyncGovtDealsRepository = govt_deal_repo   # input_table
        self._bld_deal_reop: SyncBuildingDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()

    def execute(self):
        today = date.today()
        govt_apt_rents: list[GovtAptRentsJoinKeyEntity] = self._govt_deal_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.APT_RENTS_INPUT.value
        )

        # Transfer
        apt_rents: list[AptRentModel] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.APT_DEALS_INPUT.value,
            entities=govt_apt_rents)

        self._bld_deal_reop.save_all(models=apt_rents)
