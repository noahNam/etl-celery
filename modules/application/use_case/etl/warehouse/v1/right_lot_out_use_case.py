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
    GovtRightLotOutJoinKeyEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import (
    RightLotOutModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_right_lot_out_model import (
    GovtRightLotOutModel,
)
from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals


class RightLotOutUseCase(BaseETLUseCase):
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
        govt_right_lot_outs: list[
            GovtRightLotOutJoinKeyEntity
        ] = self._govt_deal_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value
        )
        if not govt_right_lot_outs:
            print("govt_right_lot_outs 업데이트 필요한 데이터 없음")
            return

        house_ids = list()
        for govt_apt_rent in govt_right_lot_outs:
            house_ids.append(govt_apt_rent.house_id)

        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_house_ids(house_ids=house_ids)

        # Transfer
        results: tuple[
            list[RightLotOutModel], list[int]
        ] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value,
            entities=govt_right_lot_outs,
            supply_areas=supply_areas,
        )

        right_lot_outs: list[RightLotOutModel] = results[0]
        govt_right_lot_out_ids: list[int] = results[1]

        # Load
        self._bld_deal_reop.save_all(
            insert_models=right_lot_outs,
            ids=govt_right_lot_out_ids,
            update_model=GovtRightLotOutModel,
        )
