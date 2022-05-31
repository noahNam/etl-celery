from sqlalchemy import Column, BigInteger, Integer, String, Numeric, ForeignKey

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)


class DongInfoModel(warehouse_base, TimestampMixin):
    __tablename__ = "dong_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, nullable=False, autoincrement=True
    )
    house_id = Column(
        BigInteger, ForeignKey(BasicInfoModel.house_id), nullable=False, index=True
    )
    name = Column(String(30), nullable=True)
    hhld_cnt = Column(Numeric(5), nullable=True)
    grnd_flr_cnt = Column(Numeric(5), nullable=True)
