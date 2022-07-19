from sqlalchemy import Column, String, BigInteger, Integer, DECIMAL
from sqlalchemy.dialects.mysql import TIMESTAMP

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class AptDealKakaoHistoryModel(datalake_base, TimestampMixin):
    __tablename__ = "apt_deal_kakao_histories"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    regional_cd = Column(String(5), nullable=False, index=True)
    sido_sigungu = Column(String(20), nullable=False)
    dong = Column(String(10), nullable=True)
    jibun = Column(String(10), nullable=True)
    search_apt_name = Column(String(100), nullable=False)
    x_vl = Column(DECIMAL(11, 7), nullable=True)
    y_vl = Column(DECIMAL(11, 7), nullable=True)
    jibun_address = Column(String(200), nullable=True)
    road_address = Column(String(200), nullable=True)
    bld_name = Column(String(100), nullable=True)
