from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtOfctlRentsEntity
)


class GovtOfctlRentModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_ofctl_rents"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_year = Column(String(4), nullable=True)
    ofctl_name = Column(String(40), nullable=True)
    dong = Column(String(40), nullable=True)
    deposit = Column(Integer, nullable=True)
    sigungu = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    monthly_amount = Column(Integer, nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)

    def to_entity_for_bld_mapping_results(self) -> GovtOfctlRentsEntity:
        return GovtOfctlRentsEntity(
            id=self.id,
            regional_cd=self.regional_cd,
            dong=self.dong,
            jibun=self.jibun,
            ofctl_name=self.ofctl_name
        )
