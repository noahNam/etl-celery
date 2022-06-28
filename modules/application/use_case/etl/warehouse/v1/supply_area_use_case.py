from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)


class DealSupplyAreaUseCase(BaseETLUseCase):
    def __init__(self, basic_repo, bld_deal_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._basic_repo: SyncBasicRepository = basic_repo
        self._bld_deal_reop: SyncBldDealRepository = bld_deal_repo

    def execute(self):
        """
        apt_deals, apt_rents, ofctl_deals, ofctl_rents, right_lot_outs
        다섯개 테이블의 supply_area 컬럼 업데이트

        type_infos 에서 updqte_needed가 True인 것들만 가져옴
        house_id를 이용해 매핑함
        update 이후에 type_infos의 updqte_needed를 갱신하지는 않음
        """
        supply_areas: list[
            SupplyAreaEntity
        ] = self._basic_repo.find_supply_areas_by_update_needed()

        if supply_areas:
            self._bld_deal_reop.update_supply_area(supply_areas=supply_areas)
