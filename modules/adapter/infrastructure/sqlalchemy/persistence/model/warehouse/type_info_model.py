from sqlalchemy import Column, BigInteger, Integer, ForeignKey, Numeric, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    TypeInfoEntity,
)
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
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_type_info_entity(self) -> TypeInfoEntity:
        return TypeInfoEntity(
            id=self.id,
            dong_id=self.dong_id,
            private_area=self.private_area,
            supply_area=self.supply_area,
            update_needed=self.update_needed,
        )
