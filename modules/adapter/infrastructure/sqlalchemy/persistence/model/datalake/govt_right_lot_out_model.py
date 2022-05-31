from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GovtRightLotOutModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_right_lot_outs"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True, autoincrement=True
    )
    deal_amount = Column(Integer, nullable=True)
    classification_owner_ship = Column(String(2), nullable=True)
    deal_year = Column(String(4), nullable=True)
    name = Column(String(40), nullable=True)
    dong = Column(String(40), nullable=True)
    sigungu = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
