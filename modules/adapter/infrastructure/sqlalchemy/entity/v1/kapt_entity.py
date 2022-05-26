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
    place_id: int
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
    ele_manage_type: str | None
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
    name: str | None
    kaptd_wtimebus: str | None
    subway_line: str | None
    subway_station: str | None
    kaptd_wtimesub: str | None
    convenient_facility: str | None
    education_facility: str | None
    created_at: datetime
    updated_at: datetime
