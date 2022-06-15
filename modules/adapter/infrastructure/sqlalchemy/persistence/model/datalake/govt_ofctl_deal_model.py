from sqlalchemy import Column, String, BigInteger, Integer

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtOfctlDealsEntity
)


class GovtOfctlDealModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_ofctl_deals"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_amount = Column(Integer, nullable=True)
    deal_year = Column(String(4), nullable=True)
    ofctl_name = Column(String(40), nullable=True)
    dong = Column(String(40), nullable=True)
    sigungu = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    cancel_deal_type = Column(String(1), nullable=True)
    cancel_deal_day = Column(String(8), nullable=True)
    req_gbn = Column(String(10), nullable=True)
    rdealer_lawdnm = Column(String(150), nullable=True)

    def to_entity_for_bld_mapping_results(self) -> GovtOfctlDealsEntity:
        return GovtOfctlDealsEntity(
            id=self.id,
            regional_cd=self.regional_cd,
            dong=self.dong,
            jibun=self.jibun,
            ofctl_name=self.ofctl_name
        )
