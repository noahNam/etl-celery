from sqlalchemy import Column, BigInteger, Integer, String, Numeric, ForeignKey, Boolean, SmallInteger

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    DongInfoEntity, SupplyAreaEntity
)
from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from sqlalchemy.orm import relationship


class DongInfoModel(warehouse_base, TimestampMixin):
    __tablename__ = "dong_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    house_id = Column(
        BigInteger, ForeignKey(BasicInfoModel.house_id), nullable=False, index=True
    )
    name = Column(String(30), nullable=True)
    hhld_cnt = Column(SmallInteger, nullable=True)
    grnd_flr_cnt = Column(SmallInteger, nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    type_infos = relationship("TypeInfoModel",
                              backref="dong_infos", uselist=False, lazy='joined',
                              primaryjoin="foreign(DongInfoModel.id) == TypeInfoModel.dong_id"
                              )

    def to_dong_info_entity(self) -> DongInfoEntity:
        return DongInfoEntity(
            id=self.id,
            house_id=self.house_id,
            name=self.name,
            hhld_cnt=self.hhld_cnt,
            grnd_flr_cnt=self.grnd_flr_cnt,
            update_needed=self.update_needed,
        )

    def to_supply_area_entity(self) -> SupplyAreaEntity:
        return SupplyAreaEntity(
            house_id=self.house_id,
            supply_area=self.type_infos.supply_area
        )
