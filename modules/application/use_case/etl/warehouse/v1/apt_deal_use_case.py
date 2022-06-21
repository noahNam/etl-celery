from datetime import date

from modules.application.use_case.etl import BaseETLUseCase

from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealsRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsJoinKeyEntity
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel

from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class AptDealUseCase(BaseETLUseCase):
    def __init__(self, govt_deal_repo, bld_mapping_repo, bld_deal_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bld_mapping_repo: SyncBldMappingResultsRepository = bld_mapping_repo  # input_table
        self._govt_deal_repo: SyncGovtDealsRepository = govt_deal_repo   # input_table
        self._bld_deal_reop: SyncBldDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()

    def execute(self):
        #Extract
        today = date.today()
        govt_apt_deals: list[GovtAptDealsJoinKeyEntity] = self._govt_deal_repo.find_by_update_needed(
            target_date=today,
            find_type=GovtFindTypeEnum.APT_DEALS_INPUT.value
        )

        # Transfer
        apt_daels: list[AptDealModel] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.APT_DEALS_INPUT.value,
            entities=govt_apt_deals)

        # Load
        self._bld_deal_reop.save_all(models=apt_daels)



