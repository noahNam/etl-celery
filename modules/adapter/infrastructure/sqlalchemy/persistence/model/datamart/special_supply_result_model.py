from sqlalchemy import Column, String, BigInteger, Integer, Numeric, ForeignKey, Boolean

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class SpecialSupplyResultModel(datamart_base, TimestampMixin):
    __tablename__ = "special_supply_results"

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
    multi_children_vol = Column(Numeric(5), nullable=True)
    newlywed_vol = Column(Numeric(5), nullable=True)
    old_parent_vol = Column(Numeric(5), nullable=True)
    first_life_vol = Column(Numeric(5), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            public_sale_detail_id=self.public_sale_detail_id,
            region=self.region,
            region_percent=self.region_percent,
            multi_children_vol=self.multi_children_vol,
            newlywed_vol=self.newlywed_vol,
            old_parent_vol=self.old_parent_vol,
            first_life_vol=self.first_life_vol,
            update_needed=self.update_needed,
        )
