from typing import Type, Any

from sqlalchemy import update, exc, desc
from sqlalchemy.exc import StatementError
from sqlalchemy.future import select

from core.domain.warehouse.basic.interface.basic_repository import BasicRepository
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
    CalcMgmtCostEntity,
    DongInfoEntity,
    TypeInfoEntity,
    SupplyAreaEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import (
    MgmtCostModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.type_info_model import (
    TypeInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import (
    DongInfoModel as MartDongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.type_info_model import (
    TypeInfoModel as MartTypeInfoModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncBasicRepository(BasicRepository):
    def save(
        self,
        value: BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel,
    ) -> None:
        session.add(value)

    def update(
        self,
        value: BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel,
    ) -> None:
        if isinstance(value, BasicInfoModel):
            session.execute(
                update(BasicInfoModel)
                .where(BasicInfoModel.kapt_code == value.kapt_code)
                .values(
                    sido=value.sido,
                    sigungu=value.sigungu,
                    eubmyun=value.eubmyun,
                    dongri=value.dongri,
                    name=value.name,
                    bld_name=value.bld_name,
                    code_apt_nm=value.code_apt_nm,
                    origin_dong_address=value.origin_dong_address,
                    origin_road_address=value.origin_road_address,
                    new_dong_address=value.new_dong_address,
                    new_road_address=value.new_road_address,
                    place_dong_address=value.place_dong_address,
                    place_road_address=value.place_road_address,
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
                    update_needed=True,
                )
            )

        elif isinstance(value, MgmtCostModel):
            session.execute(
                update(MgmtCostModel)
                .where(MgmtCostModel.id == value.id)
                .values(
                    common_manage_cost=value.common_manage_cost,
                    individual_fee=value.individual_fee,
                    public_part_imp_cost=value.public_part_imp_cost,
                    etc_income_amount=value.etc_income_amount,
                    update_needed=True,
                )
            )

        elif isinstance(value, DongInfoModel):
            session.execute(
                update(DongInfoModel)
                .where(
                    DongInfoModel.house_id == value.house_id,
                    DongInfoModel.name == value.name,
                )
                .values(
                    hhld_cnt=value.hhld_cnt,
                    grnd_flr_cnt=value.grnd_flr_cnt,
                    update_needed=True,
                )
            )

        elif isinstance(value, TypeInfoModel):
            session.execute(
                update(TypeInfoModel)
                .where(
                    TypeInfoModel.dong_id == value.dong_id,
                    TypeInfoModel.private_area == value.private_area,
                )
                .values(
                    supply_area=value.supply_area,
                    update_needed=True,
                )
            )

    def dynamic_update(self, value: dict) -> None:
        key = value.get("key")
        items = value.get("items")
        query = select(BasicInfoModel).where(BasicInfoModel.house_id == key)
        col_info = session.execute(query).scalars().first()

        if col_info:
            for (key, value) in items.items():
                if hasattr(BasicInfoModel, key):
                    setattr(col_info, key, value)

    def exists_by_key(
        self, value: BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
    ) -> bool:
        result = None
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
                    TypeInfoModel.private_area == value.private_area,
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
        query = (
            select(BasicInfoModel.house_id)
            .where(BasicInfoModel.kapt_code == kapt_code)
            .limit(1)
        )
        house_id = session.execute(query).scalars().first()

        if not house_id:
            return None

        return house_id

    def find_to_update(
        self,
        target_model: Type[BasicInfoModel | MartDongInfoModel | MartTypeInfoModel],
    ) -> list[BasicInfoEntity | DongInfoEntity | TypeInfoEntity] | None:
        result_list = None

        if target_model == BasicInfoModel:
            query = select(BasicInfoModel).where(
                BasicInfoModel.update_needed == True,
                BasicInfoModel.place_id != None,
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_basic_info_entity() for result in results]

        elif target_model == DongInfoModel:
            query = select(DongInfoModel).where(
                DongInfoModel.update_needed == True,
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_dong_info_entity() for result in results]

        elif target_model == TypeInfoModel:
            query = select(TypeInfoModel).where(
                TypeInfoModel.update_needed == True,
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_type_info_entity() for result in results]

        return result_list

    def find_all(
        self, target_model: Type[MgmtCostModel], id: int | None, options: Any
    ) -> list[CalcMgmtCostEntity] | None:
        if target_model == MgmtCostModel:
            queryset = (
                session.execute(
                    select(MgmtCostModel)
                    .where(target_model.house_id == id)
                    .order_by(desc(MgmtCostModel.payment_date))
                )
                .scalars()
                .all()
            )

            if not queryset:
                return None

            return [
                query.to_calc_mgmt_cost_entity(priv_area=options) for query in queryset
            ]

    def change_update_needed_status(
        self, value: PrivateSaleModel | MartDongInfoModel | MartTypeInfoModel
    ) -> None:
        try:
            if isinstance(value, PrivateSaleModel):
                session.execute(
                    update(BasicInfoModel)
                    .where(BasicInfoModel.house_id == value.id)
                    .values(
                        update_needed=False,
                    )
                )

            elif isinstance(value, MartDongInfoModel):
                session.execute(
                    update(DongInfoModel)
                    .where(DongInfoModel.id == value.id)
                    .values(
                        update_needed=False,
                    )
                )

            elif isinstance(value, MartTypeInfoModel):
                session.execute(
                    update(TypeInfoModel)
                    .where(TypeInfoModel.id == value.id)
                    .values(
                        update_needed=False,
                    )
                )

            session.commit()

        except exc.IntegrityError | StatementError as e:
            logger.error(
                f"[SyncBasicRepository] change_update_needed_status -> {type(value)} error : {e}"
            )
            session.rollback()
            raise

    def find_supply_areas_by_house_ids(
        self, house_ids: list[int]
    ) -> list[SupplyAreaEntity] | None:
        house_ids = list(set(house_ids))

        querysets = list()
        for i in range(0, len(house_ids), 500):
            query = select(DongInfoModel).where(DongInfoModel.house_id.in_(house_ids))
            supply_areas = session.execute(query).scalars().all()
            querysets.extend(supply_areas)

        if not querysets:
            return None

        return [queryset.to_supply_area_entity() for queryset in querysets]

    def find_supply_areas_by_update_needed(self) -> list[SupplyAreaEntity] | None:
        query = (
            select(DongInfoModel)
            .join(TypeInfoModel, TypeInfoModel.dong_id == DongInfoModel.id)
            .where(TypeInfoModel.update_needed == True)
        )

        supply_areas = session.execute(query).scalars().all()

        if not supply_areas:
            return None

        return [supply_area.to_supply_area_entity() for supply_area in supply_areas]

    def find_id_by_dong_nm(self, house_id: int, dong_nm: str) -> int | None:
        query = (
            select(DongInfoModel.id)
            .where(
                DongInfoModel.house_id == house_id,
                DongInfoModel.name == dong_nm,
            )
            .limit(1)
        )
        dong_id = session.execute(query).scalars().first()

        if not dong_id:
            return None

        return dong_id
