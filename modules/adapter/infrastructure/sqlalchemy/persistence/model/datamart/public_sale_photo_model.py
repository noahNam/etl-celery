from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    SmallInteger,
    ForeignKey,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PublicSalePhotoModel(datamart_base, TimestampMixin):
    __tablename__ = "public_sale_photos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    public_sale_id = Column(
        BigInteger, ForeignKey(PublicSaleModel.id), nullable=False, index=True
    )
    file_name = Column(String(20), nullable=True)
    path = Column(String(150), nullable=True)
    extension = Column(String(4), nullable=True)
    is_thumbnail = Column(Boolean, nullable=True)
    seq = Column(SmallInteger, nullable=True)
    is_available = Column(Boolean, nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            public_sale_id=self.public_sale_id,
            file_name=self.file_name,
            path=self.path,
            extension=self.extension,
            is_thumbnail=self.is_thumbnail,
            seq=self.seq,
            is_available=self.is_available,
            update_needed=self.update_needed,
        )
