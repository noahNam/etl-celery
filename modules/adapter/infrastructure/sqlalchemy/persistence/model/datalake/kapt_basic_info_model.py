from sqlalchemy import Column, BigInteger, Integer, String, SmallInteger, Boolean
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptOpenApiInputEntity,
    KakaoApiInputEntity,
    KaptBasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class KaptBasicInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "kapt_basic_infos"

    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, nullable=False
    )
    kapt_code = Column(String(16), nullable=True)
    sido = Column(String(8), nullable=True)
    sigungu = Column(String(8), nullable=True)
    eubmyun = Column(String(4), nullable=True)
    dongri = Column(String(8), nullable=True)
    name = Column(String(32), nullable=True)
    code_apt_nm = Column(String(16), nullable=True)
    origin_dong_address = Column(String(100), nullable=True)
    origin_road_address = Column(String(100), nullable=True)
    new_dong_address = Column(String(100), nullable=True)
    new_road_address = Column(String(100), nullable=True)
    place_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), index=True, nullable=True
    )
    right_lot_out_type = Column(String(16), nullable=True)
    use_apr_day = Column(String(8), nullable=True)
    dong_cnt = Column(SmallInteger, nullable=True)
    hhld_cnt = Column(SmallInteger, nullable=True)
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
    update_needed = Column(Boolean, nullable=False, default=True)

    # relationship
    kapt_mgmt_costs = relationship(
        "KaptMgmtCostModel",
        backref="kapt_basic_infos",
        uselist=True,
        primaryjoin="KaptBasicInfoModel.kapt_code == foreign(KaptMgmtCostModel.kapt_code)",
    )

    def to_open_api_input_entity(self) -> KaptOpenApiInputEntity:
        return KaptOpenApiInputEntity(
            house_id=self.house_id, kapt_code=self.kapt_code, name=self.name
        )

    def to_kakao_api_input_entity(self) -> KakaoApiInputEntity:
        return KakaoApiInputEntity(
            house_id=self.house_id,
            kapt_code=self.kapt_code,
            name=self.name,
            origin_dong_address=self.origin_dong_address,
            origin_road_address=self.origin_road_address,
            new_dong_address=self.new_dong_address,
            new_road_address=self.new_road_address,
        )

    def to_kapt_basic_info_entity(self) -> KaptBasicInfoEntity:
        return KaptBasicInfoEntity(
            house_id=self.house_id,
            kapt_code=self.kapt_code,
            sido=self.sido,
            sigungu=self.sigungu,
            eubmyun=self.eubmyun,
            dongri=self.dongri,
            name=self.name,
            code_apt_nm=self.code_apt_nm,
            origin_dong_address=self.origin_dong_address,
            origin_road_address=self.origin_road_address,
            new_dong_address=self.new_dong_address,
            new_road_address=self.new_road_address,
            place_id=self.place_id,
            right_lot_out_type=self.right_lot_out_type,
            use_apr_day=self.use_apr_day,
            dong_cnt=self.dong_cnt,
            hhld_cnt=self.hhld_cnt,
            manage_type=self.manage_type,
            heat_type=self.heat_type,
            hallway_type=self.hallway_type,
            builder=self.builder,
            agency=self.agency,
            house_contractor=self.house_contractor,
            general_manage_type=self.general_manage_type,
            general_people=self.general_people,
            security_manage_type=self.security_manage_type,
            security_people=self.security_people,
            security_company=self.security_company,
            cleaning_manage_type=self.cleaning_manage_type,
            cleaning_people=self.cleaning_people,
            dispose_food=self.dispose_food,
            disinfection_manage_type=self.disinfection_manage_type,
            disinfection_per_year=self.disinfection_per_year,
            disinfection_method=self.disinfection_method,
            building_structure=self.building_structure,
            ele_capacity=self.ele_capacity,
            ele_contract_method=self.ele_contract_method,
            ele_manager_yn=self.ele_manager_yn,
            fire_reception_system=self.fire_reception_system,
            water_supply_system=self.water_supply_system,
            elv_manage_type=self.elv_manage_type,
            elv_passenger=self.elv_passenger,
            elv_freight=self.elv_freight,
            elv_merge=self.elv_merge,
            elv_handicapped=self.elv_handicapped,
            elv_emergency=self.elv_emergency,
            elv_etc=self.elv_etc,
            park_total_cnt=self.park_total_cnt,
            park_ground_cnt=self.park_ground_cnt,
            park_underground_cnt=self.park_underground_cnt,
            cctv_cnt=self.cctv_cnt,
            home_network=self.home_network,
            manage_office_address=self.manage_office_address,
            manage_office_contact=self.manage_office_contact,
            manage_office_fax=self.manage_office_fax,
            welfare=self.welfare,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
