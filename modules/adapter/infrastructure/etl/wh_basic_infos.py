from typing import Type, Any

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptBasicInfoEntity,
    KaptAreaInfoEntity,
    KaptLocationInfoEntity,
    KaptMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import (
    MgmtCostModel,
)


class TransformBasic:
    def start_etl(
        self,
        from_model: str,
        target_list: list[
            KaptBasicInfoEntity
            | KaptAreaInfoEntity
            | KaptLocationInfoEntity
            | KaptMgmtCostEntity
        ],
    ) -> list[Any] | None:
        if not target_list:
            return None

        if from_model == "kapt_basic_infos":
            return self._etl_kapt_basic_infos(target_list)
        elif from_model == "kapt_mgmt_costs":
            return self._etl_kapt_mgmt_costs(target_list)
        elif from_model == "kapt_location_infos":
            return self._etl_kapt_location_infos(target_list)
        elif from_model == "kapt_area_infos":
            return self._etl_kapt_area_infos(target_list)
        # DongInfoModel <- govt_bld_middle_infos
        # TypeInfoModel <- govt_bld_area_infos

    def _etl_kapt_mgmt_costs(
        self, target_list: list[KaptMgmtCostEntity]
    ) -> list[MgmtCostModel]:
        result = list()
        for target_entity in target_list:
            result.append(
                MgmtCostModel(
                    house_id=target_entity.house_id,
                    payment_date=target_entity.payment_date,
                    common_manage_cost=target_entity.common_manage_cost,
                    individual_fee=target_entity.individual_fee,
                    public_part_imp_cost=target_entity.public_part_imp_cost,
                    etc_income_amount=target_entity.etc_income_amount,
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
                        kaptd_wtimebus=target_entity.kaptd_wtimebus,
                        subway_line=target_entity.subway_line,
                        subway_station=target_entity.subway_station,
                        kaptd_wtimesub=target_entity.kaptd_wtimesub,
                        convenient_facility=target_entity.convenient_facility,
                        education_facility=target_entity.education_facility,
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
                        priv_area=target_entity.priv_area,
                        bjdong_cd=target_entity.bjd_code,
                    ),
                )
            )
        return result

    def _etl_kapt_basic_infos(
        self, target_list: list[KaptBasicInfoEntity]
    ) -> list[BasicInfoModel]:
        result = list()
        for target_entity in target_list:
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
                    # road_number=target_entity.road_number,
                    # road_name=target_entity.road_name,
                    # land_number=target_entity.land_number,
                )
            )
        return result

    # def __get_etl_target_schemas(self, date: str) -> dict[
    #     Type[KaptBasicInfoModel | KaptAreaInfoModel | KaptLocationInfoModel | KaptMgmtCostModel], list[
    #         KaptBasicInfoEntity | KaptAreaInfoEntity | KaptLocationInfoEntity | KaptMgmtCostEntity] | None]:
    #
    #     send_message(
    #         topic_name=ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value,
    #         date=date,
    #     )
    #     return event_listener_dict.get(
    #         f"{ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value}"
    #     )

    # BasicInfoModel(
    #     house_id=kapt_basic_info.house_id,
    #     kapt_code=kapt_basic_info.kapt_code,
    #     sido=kapt_basic_info.sido,
    #     sigungu=kapt_basic_info.sigungu,
    #     eubmyun=kapt_basic_info.eubmyun,
    #     dongri=kapt_basic_info.dongri,
    #     name=kapt_basic_info.name,
    #     code_apt_nm=kapt_basic_info.code_apt_nm,
    #     origin_dong_address=kapt_basic_info.origin_dong_address,
    #     origin_road_address=kapt_basic_info.origin_road_address,
    #     new_dong_address=kapt_basic_info.new_dong_address,
    #     new_road_address=kapt_basic_info.new_road_address,
    #     place_id=kapt_basic_info.place_id,
    #     right_lot_out_type=kapt_basic_info.right_lot_out_type,
    #     use_apr_day=kapt_basic_info.use_apr_day,
    #     dong_cnt=kapt_basic_info.dong_cnt,
    #     hhld_cnt=kapt_basic_info.hhld_cnt,
    #     manage_type=kapt_basic_info.manage_type,
    #     heat_type=kapt_basic_info.heat_type,
    #     hallway_type=kapt_basic_info.hallway_type,
    #     builder=kapt_basic_info.builder,
    #     agency=kapt_basic_info.agency,
    #     house_contractor=kapt_basic_info.house_contractor,
    #     general_manage_type=kapt_basic_info.general_manage_type,
    #     general_people=kapt_basic_info.general_people,
    #     security_manage_type=kapt_basic_info.security_manage_type,
    #     security_people=kapt_basic_info.security_people,
    #     security_company=kapt_basic_info.security_company,
    #     cleaning_manage_type=kapt_basic_info.cleaning_manage_type,
    #     cleaning_people=kapt_basic_info.cleaning_people,
    #     dispose_food=kapt_basic_info.dispose_food,
    #     disinfection_manage_type=kapt_basic_info.disinfection_manage_type,
    #     disinfection_per_year=kapt_basic_info.disinfection_per_year,
    #     disinfection_method=kapt_basic_info.disinfection_method,
    #     building_structure=kapt_basic_info.building_structure,
    #     ele_capacity=kapt_basic_info.ele_capacity,
    #     ele_contract_method=kapt_basic_info.ele_contract_method,
    #     ele_manager_yn=kapt_basic_info.ele_manager_yn,
    #     fire_reception_system=kapt_basic_info.fire_reception_system,
    #     water_supply_system=kapt_basic_info.water_supply_system,
    #     elv_manage_type=kapt_basic_info.elv_manage_type,
    #     elv_passenger=kapt_basic_info.elv_passenger,
    #     elv_freight=kapt_basic_info.elv_freight,
    #     elv_merge=kapt_basic_info.elv_merge,
    #     elv_handicapped=kapt_basic_info.elv_handicapped,
    #     elv_emergency=kapt_basic_info.elv_emergency,
    #     elv_etc=kapt_basic_info.elv_etc,
    #     park_total_cnt=kapt_basic_info.park_total_cnt,
    #     park_ground_cnt=kapt_basic_info.park_ground_cnt,
    #     park_underground_cnt=kapt_basic_info.park_underground_cnt,
    #     cctv_cnt=kapt_basic_info.cctv_cnt,
    #     home_network=kapt_basic_info.home_network,
    #     manage_office_address=kapt_basic_info.manage_office_address,
    #     manage_office_contact=kapt_basic_info.manage_office_contact,
    #     manage_office_fax=kapt_basic_info.manage_office_fax,
    #     welfare=kapt_basic_info.welfare,
    #
    #     road_number=kapt_basic_info.road_number,
    #     road_name=kapt_basic_info.road_name,
    #     land_number=kapt_basic_info.land_number,
    #     # kapt_basic_infos ############################################################
    #     x_vl=kapt_basic_info.x_vl,
    #     y_vl=kapt_basic_info.y_vl,
    #     # kakao_api_results ###########################################################
    #     sigungu_cd=kapt_basic_info.sigungu_cd,
    #     bun=kapt_basic_info.bun,
    #     ji=kapt_basic_info.ji,
    #     vl_rat=kapt_basic_info.vl_rat,
    #     bc_rat=kapt_basic_info.bc_rat,
    #     bjdong_cd=kapt_basic_info.bjdong_cd,
    #     # govt_bld_top_infos ##########################################################
    #     priv_area=kapt_basic_info.priv_area,
    #     # kapt_area_infos #############################################################
    #     kaptd_wtimebus=kapt_basic_info.kaptd_wtimebus,
    #     subway_line=kapt_basic_info.subway_line,
    #     subway_station=kapt_basic_info.subway_station,
    #     kaptd_wtimesub=kapt_basic_info.kaptd_wtimesub,
    #     convenient_facility=kapt_basic_info.convenient_facility,
    #     education_facility=kapt_basic_info.education_facility,
    #     # kapt_location_infos #########################################################
    # )
