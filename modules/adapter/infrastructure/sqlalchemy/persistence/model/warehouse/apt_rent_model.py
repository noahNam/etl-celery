from sqlalchemy import Column, String, BigInteger, Integer, Float, Boolean, Numeric

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import (
    AptRentEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class AptRentModel(warehouse_base, TimestampMixin):
    __tablename__ = "apt_rents"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    dong = Column(String(40), nullable=True)
    bld_name = Column(String(40), nullable=True)
    monthly_amount = Column(Integer, nullable=True)
    deal_year = Column(String(4), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    deposit = Column(Integer, nullable=True)
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    is_available = Column(Boolean, nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_apt_deal_entity(self) -> AptRentEntity:
        return AptRentEntity(
            id=self.id,
            house_id=self.house_id,
            dong=self.dong,
            bld_name=self.bld_name,
            monthly_amount=self.monthly_amount,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            deposit=self.deposit,
            private_area=self.private_area,
            supply_area=self.supply_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
            is_available=self.is_available,
            update_needed=self.update_needed,
        )
