from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class LegalDongCodeModel(datalake_base, TimestampMixin):
    __tablename__ = "legal_dong_codes"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False)
    region_cd = Column(String(10), nullable=True)
    sido_cd = Column(String(2), nullable=True)
    sgg_cd = Column(String(3), nullable=True)
    umd_cd = Column(String(3), nullable=True)
    ri_cd = Column(String(2), nullable=True)
    locatjumin_cd = Column(String(10), nullable=True)
    locatjijuk_cd = Column(String(10), nullable=True)
    locatadd_nm = Column(String(50), nullable=True)
    locat_order = Column(String(3), nullable=True)
    locat_rm = Column(String(200), nullable=True)
    locathigh_cd = Column(String(10), nullable=True)
    locallow_nm = Column(String(20), nullable=True)
    adpt_de = Column(String(8), nullable=True)
