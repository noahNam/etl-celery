from pydantic import BaseModel


class BasicInfoEntity(BaseModel):
    house_id: int
    kapt_code: str | None
    sido: str | None
    sigungu: str | None
    eubmyun: str | None
    dongri: str | None
    name: str | None
    bld_name: str | None
    code_apt_nm: str | None
    origin_dong_address: str | None
    origin_road_address: str | None
    new_dong_address: str | None
    new_road_address: str | None
    place_dong_address: str | None
    place_road_address: str | None
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
    x_vl: float | None
    y_vl: float | None
    road_number: str | None
    road_name: str | None
    land_number: str | None
    sigungu_cd: str | None
    bjdong_cd: str | None
    bun: str | None
    ji: str | None
    vl_rat: float | None
    bc_rat: float | None
    priv_area: str | None
    kaptd_wtimebus: str | None
    subway_line: str | None
    subway_station: str | None
    kaptd_wtimesub: str | None
    convenient_facility: str | None
    education_facility: str | None
    public_ref_id: int | None
    rebuild_ref_id: int | None
    is_available: bool | None


class CalcMgmtCostEntity(BaseModel):
    id: int
    house_id: int
    payment_date: str
    common_manage_cost: int | None = 0
    individual_fee: int | None = 0
    public_part_imp_cost: int | None = 0
    etc_income_amount: int | None = 0
    priv_area: int | None = 0  # 관리비 계산을 위한 필드 추가
    is_available: bool
