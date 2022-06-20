from sqlalchemy import Column, String, BigInteger, Integer, Numeric, ForeignKey, Boolean

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GeneralSupplyResultModel(datamart_base, TimestampMixin):
    __tablename__ = "general_supply_results"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    public_sale_detail_id = Column(
        BigInteger, ForeignKey(PublicSaleDetailModel.id), nullable=False, index=True
    )
    region = Column(String(10), nullable=True)
    region_percent = Column(Numeric(3), nullable=True)
    applicant_num = Column(Numeric(5), nullable=True)
    competition_rate = Column(Numeric(3), nullable=True)
    win_point = Column(Numeric(3), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)
