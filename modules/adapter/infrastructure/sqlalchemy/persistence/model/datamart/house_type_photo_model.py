from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    ForeignKey,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class HouseTypePhotoModel(datamart_base, TimestampMixin):
    __tablename__ = "house_type_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    private_sale_id = Column(
        BigInteger, ForeignKey(PrivateSaleModel.id), nullable=False, index=True
    )
    type_name = Column(String(20), nullable=True)
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_available = Column(Boolean, nullable=False)
    update_needed = Column(Boolean, nullable=False, default=True)
