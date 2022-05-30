from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class HouseTypePhotoModel(datalake_base, TimestampMixin):
    __tablename__ = "house_type_photos"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True)
    house_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True)
    type_name = Column(String(20), nullable=True)
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_available = Column(Boolean, nullable=True)