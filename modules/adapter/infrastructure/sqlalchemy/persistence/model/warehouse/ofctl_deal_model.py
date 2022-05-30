from sqlalchemy import Column, String, BigInteger, Integer, Float, Boolean

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class OfctlDealModel(warehouse_base, TimestampMixin):
    __tablename__ = "ofctl_deals"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
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
    private_area = Column(Float, nullable=True)
    supply_area = Column(Float, nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    cancel_deal_type = Column(String(1), nullable=True)
    cancel_deal_day = Column(String(8), nullable=True)
    req_gbn = Column(String(10), nullable=True)
    rdealer_lawdnm = Column(String(150), nullable=True)
    is_available = Column(Boolean, nullable=True)
