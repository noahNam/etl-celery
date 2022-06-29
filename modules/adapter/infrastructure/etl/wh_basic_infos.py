from typing import Any

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldTopInfoEntity,
    GovtBldMiddleInfoEntity,
    GovtBldAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptBasicInfoEntity,
    KaptAreaInfoEntity,
    KaptLocationInfoEntity,
    KaptMgmtCostEntity,
)
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
from modules.adapter.infrastructure.utils.math_helper import MathHelper


class TransformBasic:
    def start_etl(
        self,
        target_list: list[
            KaptBasicInfoEntity
            | KaptAreaInfoEntity
            | KaptLocationInfoEntity
            | KaptMgmtCostEntity
            | GovtBldTopInfoEntity
            | GovtBldMiddleInfoEntity
            | GovtBldAreaInfoEntity
        ],
    ) -> list[Any] | None:
        if not target_list:
            return None

        if isinstance(target_list[0], KaptBasicInfoEntity):
            return self._etl_kapt_basic_infos(target_list)
        elif isinstance(target_list[0], KaptMgmtCostEntity):
            return self._etl_kapt_mgmt_costs(target_list)
        elif isinstance(target_list[0], KaptLocationInfoEntity):
            return self._etl_kapt_location_infos(target_list)
        elif isinstance(target_list[0], KaptAreaInfoEntity):
            return self._etl_kapt_area_infos(target_list)
        elif isinstance(target_list[0], GovtBldTopInfoEntity):
            return self._etl_govt_bld_top_infos(target_list)
        elif isinstance(target_list[0], GovtBldMiddleInfoEntity):
            return self._etl_govt_bld_middle_infos(target_list)
        elif isinstance(target_list[0], GovtBldAreaInfoEntity):
            return self._etl_govt_bld_area_infos(target_list)

    def _etl_govt_bld_area_infos(
        self, target_list: list[GovtBldAreaInfoEntity]
    ) -> list[TypeInfoModel]:
        result = list()
        private_area = 0
        supply_area = 0
        bld_nm = None
        dong_nm = None
        ho_nm = None

        for target_entity in target_list:
            rnum = target_entity.rnum  # 1부터 시작
            if rnum == 1:
                # 변수 초기화
                bld_nm = target_entity.bld_nm
                dong_nm = target_entity.dong_nm
                ho_nm = target_entity.ho_nm
                private_area = 0
                supply_area = 0

            # 같은 건물, 동, 호인지 체크
            if (
                bld_nm != target_entity.bld_nm
                or dong_nm != target_entity.dong_nm
                or ho_nm != target_entity.ho_nm
            ):
                continue

            # 아파트인 경우는 주건축물만 취급
            if target_entity.main_atch_gb_cd != "0":  # 0(주건축물), 1(부건축물)
                continue

            if target_entity.expos_pubuse_gb_cd_nm == "전유":
                # 전유부의 경우
                private_area = (
                    target_entity.area
                    if private_area < target_entity.area
                    else private_area
                )
            else:
                # 공용부의 경우
                supply_area += target_entity.area

            result.append(
                TypeInfoModel(
                    dong_id=target_entity.dong_id,
                    private_area=MathHelper().round(private_area, 2)
                    if private_area
                    else None,
                    supply_area=MathHelper().round(supply_area, 2)
                    if supply_area
                    else None,
                    update_needed=True,
                )
            )
        return result

    def _etl_govt_bld_middle_infos(
        self, target_list: list[GovtBldMiddleInfoEntity]
    ) -> list[DongInfoModel]:
        result = list()
        for target_entity in target_list:
            result.append(
                DongInfoModel(
                    house_id=target_entity.house_id,
                    name=target_entity.dong_nm,
                    hhld_cnt=target_entity.hhld_cnt,
                    grnd_flr_cnt=target_entity.grnd_flr_cnt,
                    update_needed=True,
                )
            )
        return result

    def _etl_govt_bld_top_infos(
        self, target_list: list[GovtBldTopInfoEntity]
    ) -> list[dict]:
        result = list()
        for target_entity in target_list:
            result.append(
                dict(
                    key=target_entity.house_id,
                    items=dict(
                        bjdong_cd=target_entity.bjdong_cd,
                        sigungu_cd=target_entity.sigungu_cd,
                        bun=target_entity.bun,
                        ji=target_entity.ji,
                        bc_rat=target_entity.bc_rat,
                        vl_rat=target_entity.vl_rat,
                        update_needed=True,
                    ),
                )
            )
        return result

    def _etl_kapt_mgmt_costs(
        self, target_list: list[KaptMgmtCostEntity]
    ) -> list[MgmtCostModel]:
        result = list()
        for target_entity in target_list:
            result.append(
                MgmtCostModel(
                    id=target_entity.id,
                    house_id=target_entity.house_id,
                    payment_date=target_entity.payment_date,
                    common_manage_cost=target_entity.common_manage_cost,
                    individual_fee=target_entity.individual_fee,
                    public_part_imp_cost=target_entity.public_part_imp_cost,
                    etc_income_amount=target_entity.etc_income_amount,
                    update_needed=True,
                )
            )
        return result

    def _etl_kapt_location_infos(
        self, target_list: list[KaptLocationInfoEntity]
    ) -> list[dict]:
        result = list()
        for target_entity in target_list:
            result.append(
                dict(
                    key=target_entity.house_id,
                    items=dict(
                        kapt_code=target_entity.kapt_code,
                        kaptd_wtimebus=target_entity.kaptd_wtimebus,
                        subway_line=target_entity.subway_line,
                        subway_station=target_entity.subway_station,
                        kaptd_wtimesub=target_entity.kaptd_wtimesub,
                        convenient_facility=target_entity.convenient_facility,
                        education_facility=target_entity.education_facility,
                        update_needed=True,
                    ),
                )
            )
        return result

    def _etl_kapt_area_infos(self, target_list: list[KaptAreaInfoEntity]) -> list[dict]:
        result = list()
        for target_entity in target_list:
            result.append(
                dict(
                    key=target_entity.house_id,
                    items=dict(
                        kapt_code=target_entity.kapt_code,
                        priv_area=target_entity.priv_area,
                        bjdong_cd=target_entity.bjd_code,
                        update_needed=True,
                    ),
                )
            )
        return result

    def _etl_kapt_basic_infos(
        self, target_list: list[KaptBasicInfoEntity]
    ) -> list[BasicInfoModel]:
        result = list()

        for target_entity in target_list:
            dong_address = (
                target_entity.origin_dong_address
                if not target_entity.new_dong_address
                else target_entity.new_dong_address
            )
            road_address = (
                target_entity.origin_road_address
                if not target_entity.new_road_address
                else target_entity.new_road_address
            )

            land_number = dong_address.replace(target_entity.name, "")
            land_number = land_number.replace(target_entity.sido, "")
            land_number = land_number.replace(target_entity.sigungu, "")
            land_number = land_number.replace(target_entity.eubmyun, "")
            land_number = land_number.replace(target_entity.dongri, "")
            land_number = land_number.replace(" ", "")
            if land_number == "" or land_number == "0":
                land_number = None

            road_name = None
            road_number = None
            road_address = road_address.replace(target_entity.sido, "")
            road_address = road_address.replace(target_entity.sigungu, "")
            road_address_arr = road_address.split(" ")

            for road_addr in road_address_arr:
                if road_addr == "":
                    continue

                if "로" in road_addr:
                    road_name = road_addr
                elif "길" in road_addr:
                    road_name = road_addr
                else:
                    road_number = road_addr

            result.append(
                BasicInfoModel(
                    house_id=target_entity.house_id,
                    kapt_code=target_entity.kapt_code,
                    sido=target_entity.sido,
                    sigungu=target_entity.sigungu,
                    eubmyun=target_entity.eubmyun,
                    dongri=target_entity.dongri,
                    name=target_entity.name,
                    code_apt_nm=target_entity.code_apt_nm,
                    origin_dong_address=target_entity.origin_dong_address,
                    origin_road_address=target_entity.origin_road_address,
                    new_dong_address=target_entity.new_dong_address,
                    new_road_address=target_entity.new_road_address,
                    place_id=target_entity.place_id,
                    right_lot_out_type=target_entity.right_lot_out_type,
                    use_apr_day=target_entity.use_apr_day,
                    dong_cnt=target_entity.dong_cnt,
                    hhld_cnt=target_entity.hhld_cnt,
                    manage_type=target_entity.manage_type,
                    heat_type=target_entity.heat_type,
                    hallway_type=target_entity.hallway_type,
                    builder=target_entity.builder,
                    agency=target_entity.agency,
                    house_contractor=target_entity.house_contractor,
                    general_manage_type=target_entity.general_manage_type,
                    general_people=target_entity.general_people,
                    security_manage_type=target_entity.security_manage_type,
                    security_people=target_entity.security_people,
                    security_company=target_entity.security_company,
                    cleaning_manage_type=target_entity.cleaning_manage_type,
                    cleaning_people=target_entity.cleaning_people,
                    dispose_food=target_entity.dispose_food,
                    disinfection_manage_type=target_entity.disinfection_manage_type,
                    disinfection_per_year=target_entity.disinfection_per_year,
                    disinfection_method=target_entity.disinfection_method,
                    building_structure=target_entity.building_structure,
                    ele_capacity=target_entity.ele_capacity,
                    ele_contract_method=target_entity.ele_contract_method,
                    ele_manager_yn=target_entity.ele_manager_yn,
                    fire_reception_system=target_entity.fire_reception_system,
                    water_supply_system=target_entity.water_supply_system,
                    elv_manage_type=target_entity.elv_manage_type,
                    elv_passenger=target_entity.elv_passenger,
                    elv_freight=target_entity.elv_freight,
                    elv_merge=target_entity.elv_merge,
                    elv_handicapped=target_entity.elv_handicapped,
                    elv_emergency=target_entity.elv_emergency,
                    elv_etc=target_entity.elv_etc,
                    park_total_cnt=target_entity.park_total_cnt,
                    park_ground_cnt=target_entity.park_ground_cnt,
                    park_underground_cnt=target_entity.park_underground_cnt,
                    cctv_cnt=target_entity.cctv_cnt,
                    home_network=target_entity.home_network,
                    manage_office_address=target_entity.manage_office_address,
                    manage_office_contact=target_entity.manage_office_contact,
                    manage_office_fax=target_entity.manage_office_fax,
                    welfare=target_entity.welfare,
                    road_number=road_number,
                    road_name=road_name,
                    land_number=land_number,
                    update_needed=True,
                )
            )
        return result
