from sqlalchemy import Column, BigInteger, Integer, ForeignKey, Float, Numeric

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import (
    DongInfoModel,
)


class TypeInfoModel(warehouse_base, TimestampMixin):
    __tablename__ = "type_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    dong_id = Column(
        BigInteger, ForeignKey(DongInfoModel.house_id), nullable=False, index=True
    )
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
