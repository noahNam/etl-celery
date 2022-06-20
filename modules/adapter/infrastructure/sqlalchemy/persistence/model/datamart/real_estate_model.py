from sqlalchemy import Column, String, BigInteger, Integer, Boolean, Numeric

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class RealEstateModel(datamart_base, TimestampMixin):
    __tablename__ = "real_estates"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(String(50), nullable=True)
    jibun_address = Column(String(100), nullable=True)
    road_address = Column(String(100), nullable=True)
    si_do = Column(String(20), nullable=True)
    si_gun_gu = Column(String(16), nullable=True)
    dong_myun = Column(String(16), nullable=True)
    ri = Column(String(12), nullable=True)
    road_name = Column(String(30), nullable=True)
    road_number = Column(String(10), nullable=True)
    land_number = Column(String(10), nullable=True)
    x_vl = Column(Numeric(11, 7), nullable=False)
    y_vl = Column(Numeric(11, 7), nullable=False)
    front_legal_code = Column(String(5), nullable=False, index=True)
    back_legal_code = Column(String(5), nullable=False, index=True)
    is_available = Column(Boolean, nullable=False)
    update_needed = Column(Boolean, nullable=False, default=True)
