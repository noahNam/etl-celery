from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
)

from modules.adapter.infrastructure.sqlalchemy.entity.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
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

    def to_entity(self) -> LegalDongCodeEntity:
        return LegalDongCodeEntity(
            id=self.id,
            region_cd=self.region_cd,
            sido_cd=self.sido_cd,
            sgg_cd=self.sgg_cd,
            umd_cd=self.umd_cd,
            ri_cd=self.ri_cd,
            locatjumin_cd=self.locatjumin_cd,
            locatjijuk_cd=self.locatjijuk_cd,
            locatadd_nm=self.locatadd_nm,
            locat_order=self.locat_order,
            locat_rm=self.locat_rm,
            locathigh_cd=self.locathigh_cd,
            locallow_nm=self.locallow_nm,
            adpt_de=self.adpt_de,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
