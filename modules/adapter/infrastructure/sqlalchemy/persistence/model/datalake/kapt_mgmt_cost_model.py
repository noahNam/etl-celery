from sqlalchemy import Column, BigInteger, Integer, String, SmallInteger

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class KaptMgmtCostModel(datalake_base, TimestampMixin):
    __tablename__ = "kapt_mgmt_costs"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, nullable=False
    )
    kapt_code = Column(String(16), index=True, nullable=False)
    name = Column(String(32), nullable=True)
    payment_date = Column(String(6), index=True, nullable=False)
    common_manage_cost = Column(Integer, nullable=True)
    personnel_cost = Column(Integer, nullable=True)
    office_cost = Column(Integer, nullable=True)
    utility_cost = Column(Integer, nullable=True)
    clothe_cost = Column(Integer, nullable=True)
    edu_cost = Column(Integer, nullable=True)
    car_keep_cost = Column(Integer, nullable=True)
    etc_cost = Column(Integer, nullable=True)
    clean_cost = Column(Integer, nullable=True)
    security_cost = Column(Integer, nullable=True)
    disinfection_cost = Column(Integer, nullable=True)
    elv_keep_cost = Column(Integer, nullable=True)
    home_network_cost = Column(Integer, nullable=True)
    repair_cost = Column(Integer, nullable=True)
    facilities_keep_cost = Column(Integer, nullable=True)
    safety_check_cost = Column(Integer, nullable=True)
    disaster_prevention_cost = Column(Integer, nullable=True)
    consignment_fee = Column(Integer, nullable=True)
    individual_fee = Column(Integer, nullable=True)
    common_heat_cost = Column(Integer, nullable=True)
    dedicate_heat_cost = Column(Integer, nullable=True)
    common_water_supply_cost = Column(Integer, nullable=True)
    dedicate_water_supply_cost = Column(Integer, nullable=True)
    common_gas_cost = Column(Integer, nullable=True)
    dedicate_gas_cost = Column(Integer, nullable=True)
    common_ele_cost = Column(Integer, nullable=True)
    dedicate_ele_cost = Column(Integer, nullable=True)
    common_water_cost = Column(Integer, nullable=True)
    dedicate_water_cost = Column(Integer, nullable=True)
    septic_tank_fee = Column(Integer, nullable=True)
    waste_fee = Column(Integer, nullable=True)
    enlistment_oper_cost = Column(Integer, nullable=True)
    building_insurance_cost = Column(Integer, nullable=True)
    nec_oper_cost = Column(Integer, nullable=True)
    public_part_imp_cost = Column(Integer, nullable=True)
    public_part_usage_cost = Column(Integer, nullable=True)
    public_part_total_amount = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    public_part_save_rate = Column(Integer, nullable=True)
    etc_income_amount = Column(Integer, nullable=True)
