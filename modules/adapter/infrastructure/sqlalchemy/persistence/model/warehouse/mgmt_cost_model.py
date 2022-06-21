from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    CalcMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)


class MgmtCostModel(warehouse_base, TimestampMixin):
    __tablename__ = "mgmt_costs"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    house_id = Column(
        BigInteger, ForeignKey(BasicInfoModel.house_id), nullable=False, index=True
    )
    payment_date = Column(String(6), index=True, nullable=False)
    common_manage_cost = Column(Integer, nullable=True)
    individual_fee = Column(Integer, nullable=True)
    public_part_imp_cost = Column(Integer, nullable=True)
    etc_income_amount = Column(Integer, nullable=True)
    is_available = Column(Boolean, nullable=True, default=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_calc_mgmt_cost_entity(self, priv_area: int = None) -> CalcMgmtCostEntity:
        return CalcMgmtCostEntity(
            id=self.id,
            house_id=self.house_id,
            payment_date=self.payment_date,
            common_manage_cost=self.common_manage_cost,
            individual_fee=self.individual_fee,
            public_part_imp_cost=self.public_part_imp_cost,
            etc_income_amount=self.etc_income_amount,
            priv_area=priv_area,
            is_available=self.is_available,
            update_needed=self.update_needed,
        )
