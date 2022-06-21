from sqlalchemy import Column, BigInteger, Integer, ForeignKey, Numeric, Boolean

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class TypeInfoModel(datamart_base, TimestampMixin):
    __tablename__ = "type_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    dong_id = Column(
        BigInteger, ForeignKey(DongInfoModel.id), nullable=False, index=True
    )
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)
