from sqlalchemy import Column, String, BigInteger, Integer, Boolean
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    MappingGovtEntity,
    GovtOfctlRentJoinKeyEntity,
)


class GovtOfctlRentModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_ofctl_rents"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_year = Column(String(4), nullable=True, index=True)
    ofctl_name = Column(String(40), nullable=True)
    dong = Column(String(40), nullable=True)
    deposit = Column(Integer, nullable=True)
    sigungu = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True, index=True)
    deal_day = Column(String(6), nullable=True)
    monthly_amount = Column(Integer, nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    bld_mapping = relationship(
        "BldMappingResultModel",
        backref="govt_ofctl_rents",
        uselist=False,
        lazy="joined",
        primaryjoin="and_(foreign(GovtOfctlRentModel.regional_cd) == BldMappingResultModel.regional_cd,"
        "foreign(GovtOfctlRentModel.jibun) == BldMappingResultModel.jibun,"
        "foreign(GovtOfctlRentModel.dong) == BldMappingResultModel.dong,"
        "foreign(GovtOfctlRentModel.ofctl_name) == BldMappingResultModel.bld_name)",
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

    def to_entity_for_ofctl_rents(self) -> GovtOfctlRentJoinKeyEntity:
        return GovtOfctlRentJoinKeyEntity(
            id=self.id,
            house_id=self.bld_mapping.house_id if self.bld_mapping else None,
            dong=self.dong,
            ofctl_name=self.ofctl_name,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            deposit=self.deposit,
            monthly_amount=self.monthly_amount,
            exclusive_area=self.exclusive_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
        )
