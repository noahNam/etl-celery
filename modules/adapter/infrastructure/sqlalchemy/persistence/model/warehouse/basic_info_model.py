from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    SmallInteger,
    Numeric,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class BasicInfoModel(warehouse_base, TimestampMixin):
    __tablename__ = "basic_infos"

    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, nullable=False
    )
    kapt_code = Column(String(16), nullable=True)
    sido = Column(String(8), nullable=True)
    sigungu = Column(String(8), nullable=True)
    eubmyun = Column(String(4), nullable=True)
    dongri = Column(String(8), nullable=True)
    name = Column(String(32), nullable=True)
    code_apt_nm = Column(String(16), nullable=True, index=True)
    origin_dong_address = Column(String(100), nullable=True)
    origin_road_address = Column(String(100), nullable=True)
    new_dong_address = Column(String(100), nullable=True)
    new_road_address = Column(String(100), nullable=True)
    place_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), index=True, nullable=False
    )
    right_lot_out_type = Column(String(16), nullable=True)
    use_apr_day = Column(String(8), nullable=True)
    dong_cnt = Column(Numeric(5), nullable=True)
    hhld_cnt = Column(Numeric(5), nullable=True)
    manage_type = Column(String(16), nullable=True)
    heat_type = Column(String(8), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    builder = Column(String(64), nullable=True)
    agency = Column(String(64), nullable=True)
    house_contractor = Column(String(30), nullable=True)
    general_manage_type = Column(String(16), nullable=True)
    general_people = Column(SmallInteger, nullable=True)
    security_manage_type = Column(String(16), nullable=True)
    security_people = Column(SmallInteger, nullable=True)
    security_company = Column(String(32), nullable=True)
    cleaning_manage_type = Column(String(16), nullable=True)
    cleaning_people = Column(SmallInteger, nullable=True)
    dispose_food = Column(String(16), nullable=True)
    disinfection_manage_type = Column(String(16), nullable=True)
    disinfection_per_year = Column(SmallInteger, nullable=True)
    disinfection_method = Column(String(32), nullable=True)
    building_structure = Column(String(16), nullable=True)
    ele_capacity = Column(String(16), nullable=True)
    ele_contract_method = Column(String(4), nullable=True)
    ele_manager_yn = Column(String(4), nullable=True)
    fire_reception_system = Column(String(4), nullable=True)
    water_supply_system = Column(String(8), nullable=True)
    elv_manage_type = Column(String(16), nullable=True)
    elv_passenger = Column(SmallInteger, nullable=True)
    elv_freight = Column(SmallInteger, nullable=True)
    elv_merge = Column(SmallInteger, nullable=True)
    elv_handicapped = Column(SmallInteger, nullable=True)
    elv_emergency = Column(SmallInteger, nullable=True)
    elv_etc = Column(SmallInteger, nullable=True)
    park_total_cnt = Column(SmallInteger, nullable=True)
    park_ground_cnt = Column(SmallInteger, nullable=True)
    park_underground_cnt = Column(SmallInteger, nullable=True)
    cctv_cnt = Column(SmallInteger, nullable=True)
    home_network = Column(String(1), nullable=True)
    manage_office_address = Column(String(100), nullable=True)
    manage_office_contact = Column(String(16), nullable=True)
    manage_office_fax = Column(String(16), nullable=True)
    welfare = Column(String(200), nullable=True)
    x_vl = Column(Numeric(11, 7), nullable=True)
    y_vl = Column(Numeric(11, 7), nullable=True)
    road_number = Column(String(10), nullable=True)
    road_name = Column(String(30), nullable=True)
    land_number = Column(String(10), nullable=True)
    sigungu_cd = Column(String(5), nullable=True, index=True)
    bjdong_cd = Column(String(5), nullable=True, index=True)
    bun = Column(String(4), nullable=True)
    ji = Column(String(4), nullable=True)
    vl_rat = Column(Numeric(6, 2), nullable=True)
    bc_rat = Column(Numeric(6, 2), nullable=True)
    priv_area = Column(String(22), nullable=True)
    kaptd_wtimebus = Column(String(10), nullable=True)
    subway_line = Column(String(50), nullable=True)
    subway_station = Column(String(50), nullable=True)
    kaptd_wtimesub = Column(String(10), nullable=True)
    convenient_facility = Column(String(500), nullable=True)
    education_facility = Column(String(500), nullable=True)
    public_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    rebuild_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    is_available = Column(Boolean, nullable=True)
