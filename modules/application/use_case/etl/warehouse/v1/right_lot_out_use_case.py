from modules.adapter.infrastructure.etl.bld_deals import TransferAptDeals
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtRightLotOutJoinKeyEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_right_lot_out_model import (
    GovtRightLotOutModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import (
    RightLotOutModel,
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
from modules.adapter.infrastructure.crawler.crawler.enum.govt_deal_enum import (
    GovtHouseDealEnum,
)


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
        self._bld_mapping_repo = bld_mapping_repo
        self._govt_deal_repo: SyncGovtDealRepository = govt_deal_repo  # input_table
        self._bld_deal_reop: SyncBldDealRepository = bld_deal_repo  # result_table
        self._transfer: TransferAptDeals = TransferAptDeals()
        self._basic_repo: SyncBasicRepository = basic_repo

    def execute(self):
        # Extract
        start_year = GovtHouseDealEnum.MIN_YEAR_MONTH.value[:4]
        start_month = str(int(GovtHouseDealEnum.MIN_YEAR_MONTH.value[5:]))
        end_year = GovtHouseDealEnum.MAX_YEAR_MONTH.value[:4]
        end_month = str(int(GovtHouseDealEnum.MAX_YEAR_MONTH.value[5:]))

        govt_right_lot_outs: list[
            GovtRightLotOutJoinKeyEntity
        ] = self._govt_deal_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )
        if not govt_right_lot_outs:
            print("govt_right_lot_outs 업데이트 필요한 데이터 없음")
            return

        # house_id None filter
        new_govts: list[GovtRightLotOutJoinKeyEntity] = list()
        for govt_right_lot_out in govt_right_lot_outs:
            if govt_right_lot_out.house_id:
                new_govts.append(govt_right_lot_out)

        house_ids = list()
        for new_govt in new_govts:
            house_ids.append(new_govt.house_id)

        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_house_ids(house_ids=house_ids)

        # Transfer
        results: tuple[
            list[RightLotOutModel], list[int]
        ] = self._transfer.start_transfer(
            transfer_type=GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value,
            entities=new_govts,
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
