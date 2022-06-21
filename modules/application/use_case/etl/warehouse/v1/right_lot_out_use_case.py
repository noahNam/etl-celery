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
    GovtRightLotOutJoinKeyEntity
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel
from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class RightLotOutUseCase(BaseETLUseCase):
    def __init__(self, govt_deal_repo, bld_mapping_repo, bld_deal_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bld_mapping_repo: SyncBldMappingResultsRepository = bld_mapping_repo  # input_table
        self._govt_deal_repo: SyncGovtDealsRepository = govt_deal_repo   # input_table
        self._bld_deal_reop: SyncBuildingDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()

    def execute(self):
        today = date.today()
        govt_right_lot_outs: list[GovtRightLotOutJoinKeyEntity] = self._govt_deal_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value
        )

        ofctl_rents: list[RightLotOutModel] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.APT_DEALS_INPUT.value,
            entities=govt_right_lot_outs)

        self._bld_deal_reop.save_all(models=ofctl_rents)
