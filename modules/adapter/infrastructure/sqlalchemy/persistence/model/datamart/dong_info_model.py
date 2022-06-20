from sqlalchemy import Column, String, BigInteger, Integer, Numeric, ForeignKey, Boolean

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class DongInfoModel(datamart_base, TimestampMixin):
    __tablename__ = "dong_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    private_sale_id = Column(
        BigInteger, ForeignKey(PrivateSaleModel.id), nullable=False, index=True
    )
    name = Column(String(30), nullable=True)
    hhld_cnt = Column(Numeric(5), nullable=True)
    grnd_flr_cnt = Column(Numeric(5), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)
