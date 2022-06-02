from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GovtAptDealModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_apt_deals"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_amount = Column(Integer, nullable=True)
    build_year = Column(String(4), nullable=True)
    deal_year = Column(String(4), nullable=True)
    road_name = Column(String(40), nullable=True)
    road_name_bonbun = Column(String(5), nullable=True)
    road_name_bubun = Column(String(5), nullable=True)
    road_name_sigungu_cd = Column(String(5), nullable=True)
    road_name_seq = Column(String(2), nullable=True)
    road_name_basement_cd = Column(String(1), nullable=True)
    road_name_cd = Column(String(7), nullable=True)
    dong = Column(String(40), nullable=True)
    bonbun_cd = Column(String(4), nullable=True)
    bubun_cd = Column(String(4), nullable=True)
    sigungu_cd = Column(String(5), nullable=True)
    eubmyundong_cd = Column(String(5), nullable=True)
    land_cd = Column(String(1), nullable=True)
    apt_name = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    serial_no = Column(String(14), nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    cancel_deal_type = Column(String(1), nullable=True)
    cancel_deal_day = Column(String(8), nullable=True)
    req_gbn = Column(String(10), nullable=True)
    rdealer_lawdnm = Column(String(150), nullable=True)
