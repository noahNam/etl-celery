from sqlalchemy import Column, BigInteger, Integer, String

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class KaptMgmtCostModel(datalake_base, TimestampMixin):
    __tablename__ = "kapt_mgmt_costs"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    kapt_code = Column(String(16), index=True, nullable=False)
    name = Column(String(32), nullable=True)
    payment_date = Column(String(6), index=True, nullable=False)
    common_manage_cost = Column(Integer, nullable=True)
    personnel_cost = Column(Integer, nullable=True)
    office_cost = Column(Integer, nullable=True)
    utility_tax = Column(Integer, nullable=True)
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
    public_part_total_amount = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=True
    )
    public_part_save_rate = Column(Integer, nullable=True)
    etc_income_amount = Column(Integer, nullable=True)

    def to_kapt_mgmt_cost_entity(self) -> KaptMgmtCostEntity:
        return KaptMgmtCostEntity(
            id=self.id,
            kapt_code=self.kapt_code,
            name=self.name,
            payment_date=self.payment_date,
            common_manage_cost=self.common_manage_cost,
            personnel_cost=self.personnel_cost,
            office_cost=self.office_cost,
            utility_tax=self.utility_tax,
            clothe_cost=self.clothe_cost,
            edu_cost=self.edu_cost,
            car_keep_cost=self.car_keep_cost,
            etc_cost=self.etc_cost,
            clean_cost=self.clean_cost,
            security_cost=self.security_cost,
            disinfection_cost=self.disinfection_cost,
            elv_keep_cost=self.elv_keep_cost,
            home_network_cost=self.home_network_cost,
            repair_cost=self.repair_cost,
            facilities_keep_cost=self.facilities_keep_cost,
            safety_check_cost=self.safety_check_cost,
            disaster_prevention_cost=self.disaster_prevention_cost,
            consignment_fee=self.consignment_fee,
            individual_fee=self.individual_fee,
            common_heat_cost=self.common_heat_cost,
            dedicate_heat_cost=self.dedicate_heat_cost,
            common_water_supply_cost=self.common_water_supply_cost,
            dedicate_water_supply_cost=self.dedicate_water_supply_cost,
            common_gas_cost=self.common_gas_cost,
            dedicate_gas_cost=self.dedicate_gas_cost,
            common_ele_cost=self.common_ele_cost,
            dedicate_ele_cost=self.dedicate_ele_cost,
            common_water_cost=self.common_water_cost,
            dedicate_water_cost=self.dedicate_water_cost,
            septic_tank_fee=self.septic_tank_fee,
            waste_fee=self.waste_fee,
            enlistment_oper_cost=self.enlistment_oper_cost,
            building_insurance_cost=self.building_insurance_cost,
            nec_oper_cost=self.nec_oper_cost,
            public_part_imp_cost=self.public_part_imp_cost,
            public_part_usage_cost=self.public_part_usage_cost,
            public_part_total_amount=self.public_part_total_amount,
            public_part_save_rate=self.public_part_save_rate,
            etc_income_amount=self.etc_income_amount,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
