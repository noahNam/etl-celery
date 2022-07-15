from sqlalchemy import Column, String, BigInteger, Integer, UniqueConstraint

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class BldMappingResultModel(datalake_base, TimestampMixin):
    __tablename__ = "bld_mapping_results"
    __table_args__ = (
        UniqueConstraint(
            'regional_cd',
            'jibun',
            'dong',
            'bld_name',
            name='bld_mapping_results_unique'
        ),
    )

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    place_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=True, index=True
    )
    house_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    regional_cd = Column(String(5), nullable=True, index=True)
    jibun = Column(String(10), nullable=True)
    dong = Column(String(40), nullable=True)
    bld_name = Column(String(40), nullable=True)
