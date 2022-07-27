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
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSaleDtPhotoEntity,
)


class PublicSaleDetailPhotoModel(datalake_base, TimestampMixin):
    __tablename__ = "public_sale_detail_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    subs_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    area_type = Column(String(10), nullable=True)
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_available = Column(Boolean, nullable=True)
    update_needed = Column(Boolean, nullable=True)

    def to_entity(self) -> PublicSaleDtPhotoEntity:
        return PublicSaleDtPhotoEntity(
            id=self.id,
            sub_id=self.subs_id,
            area_type=self.area_type,
            file_name=self.file_name,
            path=self.path,
            extension=self.extension,
            is_available=self.is_available,
        )
