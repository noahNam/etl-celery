from sqlalchemy import Column, String, BigInteger, Integer, Float, Boolean, Numeric

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import OfctlDealEntity
from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class OfctlDealModel(warehouse_base, TimestampMixin):
    __tablename__ = "ofctl_deals"

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
    deal_amount = Column(Integer, nullable=True)
    deal_year = Column(String(4), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    cancel_deal_type = Column(String(1), nullable=True)
    cancel_deal_day = Column(String(8), nullable=True)
    req_gbn = Column(String(10), nullable=True)
    rdealer_lawdnm = Column(String(150), nullable=True)
    is_available = Column(Boolean, nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_ofctl_deal_entity(self) -> OfctlDealEntity:
        return OfctlDealEntity(
            id=self.id,
            house_id=self.house_id,
            dong=self.dong,
            bld_name=self.bld_name,
            deal_amount=self.deal_amount,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            private_area=self.private_area,
            supply_area=self.supply_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
            cancel_deal_type=self.cancel_deal_type,
            cancel_deal_day=self.cancel_deal_day,
            req_gbn=self.req_gbn,
            rdealer_lawdnm=self.rdealer_lawdnm,
            is_available=self.is_available,
            update_needed=self.update_needed
        )