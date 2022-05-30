from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GovtAptRentModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_apt_rents"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False)
    build_year = Column(String(4), nullable=True)
    deal_year = Column(String(4), nullable=True)
    dong = Column(String(40), nullable=True)
    deposit = Column(Integer, nullable=True)
    apt_name = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    monthly_amount = Column(Integer, nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True)
    floor = Column(String(4), nullable=True)
