from sqlalchemy import Column, String, BigInteger, Integer, Boolean
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    MappingGovtEntity,
    GovtOfctlDealJoinKeyEntity,
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
    update_needed = Column(Boolean, nullable=False, default=True)

    bld_mapping = relationship(
        "BldMappingResultModel",
        backref="govt_ofctl_deals",
        uselist=False,
        lazy="joined",
        primaryjoin="and_(foreign(GovtOfctlDealModel.regional_cd) == BldMappingResultModel.regional_cd,"
        "foreign(GovtOfctlDealModel.jibun) == BldMappingResultModel.jibun,"
        "foreign(GovtOfctlDealModel.dong) == BldMappingResultModel.dong,"
        "foreign(GovtOfctlDealModel.ofctl_name) == BldMappingResultModel.bld_name)",
    )

    def to_entity_for_bld_mapping_results(self) -> MappingGovtEntity:
        return MappingGovtEntity(
            id=self.id,
            mapping_id=self.bld_mapping.id if self.bld_mapping else None,
            regional_cd=self.regional_cd,
            dong=self.dong,
            jibun=self.jibun,
            apt_name=self.ofctl_name,
        )

    def to_entity_for_ofctl_deals(self) -> GovtOfctlDealJoinKeyEntity:
        return GovtOfctlDealJoinKeyEntity(
            id=self.id,
            house_id=self.bld_mapping.house_id if self.bld_mapping else None,
            dong=self.dong,
            ofctl_name=self.ofctl_name,
            deal_amount=self.deal_amount,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            exclusive_area=self.exclusive_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
            cancel_deal_type=self.cancel_deal_type,
            cancel_deal_day=self.cancel_deal_day,
            req_gbn=self.req_gbn,
            rdealer_lawdnm=self.rdealer_lawdnm,
        )
