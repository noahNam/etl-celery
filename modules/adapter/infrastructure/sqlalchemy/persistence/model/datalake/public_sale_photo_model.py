from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    SmallInteger,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSalePhotoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PublicSalePhotoModel(datalake_base, TimestampMixin):
    __tablename__ = "public_sale_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    subs_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_thumbnail = Column(Boolean, nullable=True)
    seq = Column(SmallInteger, nullable=True)
    is_available = Column(Boolean, nullable=True)
    update_needed = Column(Boolean, nullable=True)

    def to_entity(self) -> PublicSalePhotoEntity:
        return PublicSalePhotoEntity(
            id=self.id,
            subs_id=self.subs_id,
            file_name=self.file_name,
            path=self.path,
            extension=self.extension,
            is_thumbnail=self.is_thumbnail,
            seq=self.seq,
            is_available=self.is_available,
        )
