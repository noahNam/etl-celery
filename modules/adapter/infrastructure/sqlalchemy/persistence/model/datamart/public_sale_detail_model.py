from sqlalchemy import Column, String, BigInteger, Integer, Numeric, ForeignKey

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
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
