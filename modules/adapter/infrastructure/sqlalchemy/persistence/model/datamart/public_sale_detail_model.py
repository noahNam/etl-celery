from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Numeric,
    ForeignKey,
    Text,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datamart.v1.public_sale_entity import (
    PublicDtUniqueEntity,
)


class PublicSaleDetailModel(datamart_base, TimestampMixin):
    __tablename__ = "public_sale_details"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    public_sale_id = Column(
        BigInteger, ForeignKey(PublicSaleModel.id), nullable=False, index=True
    )
    area_type = Column(String(5), nullable=True)
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
    supply_price = Column(Integer, nullable=True)
    acquisition_tax = Column(Integer, nullable=True)
    special_household = Column(Numeric(5), nullable=True)
    multi_children_household = Column(Numeric(5), nullable=True)
    newlywed_household = Column(Numeric(5), nullable=True)
    old_parent_household = Column(Numeric(5), nullable=True)
    first_life_household = Column(Numeric(5), nullable=True)
    general_household = Column(Numeric(5), nullable=True)
    bay = Column(String(10), nullable=True)
    pansang_tower = Column(String(10), nullable=True)
    kitchen_window = Column(String(1), nullable=True)
    direct_window = Column(String(1), nullable=True)
    alpha_room = Column(String(1), nullable=True)
    cyber_model_house_link = Column(Text, nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_unique_entity(self) -> PublicDtUniqueEntity:
        return PublicDtUniqueEntity(
            id=self.id,
            public_sale_id=self.public_sale_id,
            area_type=self.area_type,
            private_area=self.private_area,
        )

    def to_dict(self):
        return dict(
            id=self.id,
            public_sale_id=self.public_sale_id,
            area_type=self.area_type,
            private_area=self.private_area,
            supply_area=self.supply_area,
            supply_price=self.supply_price,
            acquisition_tax=self.acquisition_tax,
            special_household=self.special_household,
            multi_children_household=self.multi_children_household,
            newlywed_household=self.newlywed_household,
            old_parent_household=self.old_parent_household,
            first_life_household=self.first_life_household,
            general_household=self.general_household,
            bay=self.bay,
            pansang_tower=self.pansang_tower,
            kitchen_window=self.kitchen_window,
            direct_window=self.direct_window,
            alpha_room=self.alpha_room,
            cyber_model_house_link=self.cyber_model_house_link,
            update_needed=self.update_needed,
        )
