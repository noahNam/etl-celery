from typing import Callable, ContextManager, Type
from sqlalchemy import update, exc
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from core.domain.warehouse.basic.interface.basic_repository import BasicRepository
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import (
    MgmtCostModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.type_info_model import (
    TypeInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository import (
    BaseSyncRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncBasicRepository(BasicRepository, BaseSyncRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def save(
        self,
        target_model: Type[
            BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
        ],
        value: [BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel],
    ) -> None:
        with self.session_factory() as session:
            try:
                session.add(value)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncBasicRepository][save] target_model : {target_model} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException

    def update(
        self,
        target_model: Type[
            BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
        ],
        value: [BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel],
    ) -> None:
        with self.session_factory() as session:
            if target_model == BasicInfoModel:
                session.execute(
                    update(BasicInfoModel)
                    .where(BasicInfoModel.kapt_code == value.kapt_code)
                    .values(
                        sido=value.sido,
                        sigungu=value.sigungu,
                        eubmyun=value.eubmyun,
                        dongri=value.dongri,
                        name=value.name,
                        code_apt_nm=value.code_apt_nm,
                        origin_dong_address=value.origin_dong_address,
                        origin_road_address=value.origin_road_address,
                        new_dong_address=value.new_dong_address,
                        new_road_address=value.new_road_address,
                        place_id=value.place_id,
                        right_lot_out_type=value.right_lot_out_type,
                        use_apr_day=value.use_apr_day,
                        dong_cnt=value.dong_cnt,
                        hhld_cnt=value.hhld_cnt,
                        manage_type=value.manage_type,
                        heat_type=value.heat_type,
                        hallway_type=value.hallway_type,
                        builder=value.builder,
                        agency=value.agency,
                        house_contractor=value.house_contractor,
                        general_manage_type=value.general_manage_type,
                        general_people=value.general_people,
                        security_manage_type=value.security_manage_type,
                        security_people=value.security_people,
                        security_company=value.security_company,
                        cleaning_manage_type=value.cleaning_manage_type,
                        cleaning_people=value.cleaning_people,
                        dispose_food=value.dispose_food,
                        disinfection_manage_type=value.disinfection_manage_type,
                        disinfection_per_year=value.disinfection_per_year,
                        disinfection_method=value.disinfection_method,
                        building_structure=value.building_structure,
                        ele_capacity=value.ele_capacity,
                        ele_contract_method=value.ele_contract_method,
                        ele_manager_yn=value.ele_manager_yn,
                        fire_reception_system=value.fire_reception_system,
                        water_supply_system=value.water_supply_system,
                        elv_manage_type=value.elv_manage_type,
                        elv_passenger=value.elv_passenger,
                        elv_freight=value.elv_freight,
                        elv_merge=value.elv_merge,
                        elv_handicapped=value.elv_handicapped,
                        elv_emergency=value.elv_emergency,
                        elv_etc=value.elv_etc,
                        park_total_cnt=value.park_total_cnt,
                        park_ground_cnt=value.park_ground_cnt,
                        park_underground_cnt=value.park_underground_cnt,
                        cctv_cnt=value.cctv_cnt,
                        home_network=value.home_network,
                        manage_office_address=value.manage_office_address,
                        manage_office_contact=value.manage_office_contact,
                        manage_office_fax=value.manage_office_fax,
                        welfare=value.welfare,
                        road_number=value.road_number,
                        road_name=value.road_name,
                        land_number=value.land_number,
                        x_vl=value.x_vl,
                        y_vl=value.y_vl,
                    )
                )

            elif target_model == MgmtCostModel:
                session.execute(
                    update(MgmtCostModel)
                    .where(
                        MgmtCostModel.house_id == value.house_id
                        and MgmtCostModel.payment_date == value.payment_date
                    )
                    .values(
                        common_manage_cost=value.common_manage_cost,
                        individual_fee=value.individual_fee,
                        public_part_imp_cost=value.public_part_imp_cost,
                        etc_income_amount=value.etc_income_amount,
                    )
                )

            elif target_model == DongInfoModel:
                session.execute(
                    update(DongInfoModel)
                    .where(
                        DongInfoModel.id == value.id
                    )
                    .values(
                        name=value.name,
                        hhld_cnt=value.hhld_cnt,
                        grnd_flr_cnt=value.grnd_flr_cnt,
                    )
                )

            elif target_model == TypeInfoModel:
                session.execute(
                    update(TypeInfoModel)
                    .where(
                        TypeInfoModel.id == value.id
                    )
                    .values(
                        private_area=value.private_area,
                        supply_area=value.supply_area,
                    )
                )

            session.commit()

    def dynamic_update(self, target_model: Type[BasicInfoModel], value: dict) -> None:
        with self.session_factory() as session:
            key = value.get("key")
            items = value.get("items")
            query = select(BasicInfoModel).where(target_model.house_id == key)
            col_info = session.execute(query).scalars().first()

            for (key, value) in items.items():
                if hasattr(target_model, key):
                    setattr(col_info, key, value)
                    session.commit()

    def exists_by_key(
        self, value: BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
    ) -> bool:
        with self.session_factory() as session:
            if isinstance(value, BasicInfoModel):
                query = (
                    select(BasicInfoModel.house_id)
                    .where(BasicInfoModel.kapt_code == value.kapt_code)
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

            elif isinstance(value, DongInfoModel):
                query = (
                    select(DongInfoModel.id)
                    .where(
                        DongInfoModel.house_id == value.house_id,
                        DongInfoModel.name == value.name,
                    )
                    .limit(1)
                )
                result = session.execute(query).scalars().first()
                value.id = result

            elif isinstance(value, TypeInfoModel):
                query = (
                    select(TypeInfoModel.id)
                    .where(
                        TypeInfoModel.dong_id == value.dong_id,
                        TypeInfoModel.private_area == value.private_area
                        and TypeInfoModel.supply_area == value.supply_area,
                    )
                    .limit(1)
                )
                result = session.execute(query).scalars().first()
                value.id = result

            elif isinstance(value, MgmtCostModel):
                query = (
                    select(MgmtCostModel.id)
                    .where(
                        MgmtCostModel.house_id == value.house_id,
                        MgmtCostModel.payment_date == value.payment_date,
                    )
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

        if result:
            return True

        return False

    def find_house_id_by_code(self, kapt_code: str) -> int | None:
        with self.session_factory() as session:
            query = (
                select(BasicInfoModel.house_id)
                .where(BasicInfoModel.kapt_code == kapt_code)
                .limit(1)
            )
            house_id = session.execute(query).scalars().first()

        if not house_id:
            return None

        return house_id