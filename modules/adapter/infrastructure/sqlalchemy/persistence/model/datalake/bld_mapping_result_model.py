from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class BldMappingResultModel(datalake_base, TimestampMixin):
    __tablename__ = "bld_mapping_results"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False)
    place_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False)
    house_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False)
    regional_cd = Column(String(5), nullable=True)
    dong = Column(String(40), nullable=True)
    bld_name = Column(String(40), nullable=True)
