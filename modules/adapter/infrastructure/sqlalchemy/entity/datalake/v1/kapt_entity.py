from datetime import datetime

from pydantic import BaseModel


class KaptBasicInfoEntity(BaseModel):
    house_id: int
    kapt_code: str | None
    sido: str | None
    sigungu: str | None
    eubmyun: str | None
    dongri: str | None
    name: str | None
    code_apt_nm: str | None
    origin_dong_address: str | None
    origin_road_address: str | None
    new_dong_address: str | None
    new_road_address: str | None
    place_id: int | None
    right_lot_out_type: str | None
    use_apr_day: str | None
    dong_cnt: int | None
    hhld_cnt: int | None
    manage_type: str | None
    heat_type: str | None
    hallway_type: str | None
    builder: str | None
    agency: str | None
    house_contractor: str | None
    general_manage_type: str | None
    general_people: int | None
    security_manage_type: str | None
    security_people: int | None
    security_company: str | None
    cleaning_manage_type: str | None
    cleaning_people: int | None
    dispose_food: str | None
    disinfection_manage_type: str | None
    disinfection_per_year: int | None
    disinfection_method: str | None
    building_structure: str | None
    ele_capacity: str | None
    ele_contract_method: str | None
    ele_manager_yn: str | None
    fire_reception_system: str | None
    water_supply_system: str | None
    elv_manage_type: str | None
    elv_passenger: int | None
    elv_freight: int | None
    elv_merge: int | None
    elv_handicapped: int | None
    elv_emergency: int | None
    elv_etc: int | None
    park_total_cnt: int | None
    park_ground_cnt: int | None
    park_underground_cnt: int | None
    cctv_cnt: int | None
    home_network: str | None
    manage_office_address: str | None
    manage_office_contact: str | None
    manage_office_fax: str | None
    welfare: str | None
    created_at: datetime
    updated_at: datetime


class KaptOpenApiInputEntity(BaseModel):
    house_id: int
    kapt_code: str | None
    name: str | None


class KaptAreaInfoEntity(BaseModel):
    kapt_code: str
    house_id: int | None  # schema model 에는 없지만 ETL시 관계 참조용 변수로 선언(kapt_code는 추후 다른 크롤링 방법으로 메타데이터를 끌어올때 없을 수 있음)(kapt_code는 추후 다른 크롤링 방법으로 메타데이터를 끌어올때 없을 수 있음)
    name: str | None
    kapt_tarea: str | None
    kapt_marea: str | None
    kapt_mparea_60: str | None
    kapt_mparea_85: str | None
    kapt_mparea_135: str | None
    kapt_mparea_136: str | None
    priv_area: str | None
    bjd_code: str | None
    created_at: datetime
    updated_at: datetime


class KaptLocationInfoEntity(BaseModel):
    kapt_code: str
    house_id: int | None  # schema model 에는 없지만 ETL시 관계 참조용 변수로 선언(kapt_code는 추후 다른 크롤링 방법으로 메타데이터를 끌어올때 없을 수 있음)(kapt_code는 추후 다른 크롤링 방법으로 메타데이터를 끌어올때 없을 수 있음)
    name: str | None
    kaptd_wtimebus: str | None
    subway_line: str | None
    subway_station: str | None
    kaptd_wtimesub: str | None
    convenient_facility: str | None
    education_facility: str | None
    created_at: datetime
    updated_at: datetime


class KakaoApiInputEntity(BaseModel):
    house_id: int
    kapt_code: str | None
    name: str | None
    origin_dong_address: str | None
    origin_road_address: str | None
    new_dong_address: str | None
    new_road_address: str | None


class GovtBldInputEntity(BaseModel):
    house_id: int
    kapt_code: str | None
    name: str | None
    origin_dong_address: str | None
    new_dong_address: str | None
    bjd_code: str | None


class KaptMgmtCostEntity(BaseModel):
    id: int
    kapt_code: str
    house_id: int | None  # schema model 에는 없지만 ETL시 관계 참조용 변수로 선언(kapt_code는 추후 다른 크롤링 방법으로 메타데이터를 끌어올때 없을 수 있음)
    name: str | None
    payment_date: str | None
    common_manage_cost: int | None
    personnel_cost: int | None
    office_cost: int | None
    utility_tax: int | None
    clothe_cost: int | None
    edu_cost: int | None
    car_keep_cost: int | None
    etc_cost: int | None
    clean_cost: int | None
    security_cost: int | None
    disinfection_cost: int | None
    elv_keep_cost: int | None
    home_network_cost: int | None
    repair_cost: int | None
    facilities_keep_cost: int | None
    safety_check_cost: int | None
    disaster_prevention_cost: int | None
    consignment_fee: int | None
    individual_fee: int | None
    common_heat_cost: int | None
    dedicate_heat_cost: int | None
    common_water_supply_cost: int | None
    dedicate_water_supply_cost: int | None
    common_gas_cost: int | None
    dedicate_gas_cost: int | None
    common_ele_cost: int | None
    dedicate_ele_cost: int | None
    common_water_cost: int | None
    dedicate_water_cost: int | None
    septic_tank_fee: int | None
    waste_fee: int | None
    enlistment_oper_cost: int | None
    building_insurance_cost: int | None
    nec_oper_cost: int | None
    public_part_imp_cost: int | None
    public_part_usage_cost: int | None
    public_part_total_amount: int | None
    public_part_save_rate: int | None
    etc_income_amount: int | None
    created_at: datetime
    updated_at: datetime
