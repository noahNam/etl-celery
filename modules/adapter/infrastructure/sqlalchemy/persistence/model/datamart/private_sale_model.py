from sqlalchemy import Column, String, BigInteger, Integer, Boolean, Numeric, ForeignKey, SmallInteger

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import RealEstateModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PrivateSaleModel(datamart_base, TimestampMixin):
    __tablename__ = "private_sales"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
    )
    real_estate_id = Column(BigInteger, ForeignKey(RealEstateModel.id), nullable=False, index=True)
    name = Column(String(50), nullable=True)
    building_type = Column(String(5), nullable=True)
    build_year = Column(String(4), nullable=True)
    move_in_date = Column(String(8), nullable=True)
    dong_cnt = Column(Numeric(5), nullable=True)
    hhld_cnt  = Column(Numeric(5), nullable=True)
    heat_type = Column(String(8), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    builder = Column(String(64), nullable=True)
    park_total_cnt = Column(Numeric(5), nullable=True)
    park_ground_cnt = Column(Numeric(5), nullable=True)
    park_underground_cnt  = Column(Numeric(5), nullable=True)
    cctv_cnt  = Column(Numeric(5), nullable=True)
    welfare = Column(String(200), nullable=True)
    vl_rat = Column(Numeric(4, 2), nullable=True)
    bc_rat = Column(Numeric(4, 2), nullable=True)
    summer_mgmt_cost = Column(SmallInteger, nullable=True)
    winter_mgmt_cost = Column(SmallInteger, nullable=True)
    avg_mgmt_cost = Column(SmallInteger, nullable=True)
    public_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    rebuild_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)
