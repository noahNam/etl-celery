from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    SmallInteger,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class HousePhotoModel(datalake_base, TimestampMixin):
    __tablename__ = "house_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_thumbnail = Column(Boolean, nullable=True)
    seq = Column(SmallInteger, nullable=True)
    is_available = Column(Boolean, nullable=True)
