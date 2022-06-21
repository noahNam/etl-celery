from sqlalchemy import Column, String, BigInteger, Integer, Boolean
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptRentsEntity,
    GovtAptRentsJoinKeyEntity
)


class GovtAptRentModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_apt_rents"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    build_year = Column(String(4), nullable=True)
    deal_year = Column(String(4), nullable=True)
    dong = Column(String(40), nullable=True)
    deposit = Column(Integer, nullable=True)
    apt_name = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    monthly_amount = Column(Integer, nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    bld_mapping = relationship("BldMappingResultModel",
                               backref="govt_apt_rents", uselist=False, lazy='joined',
                               primaryjoin="and_(foreign(GovtAptRentModel.regional_cd) == BldMappingResultModel.regional_cd,"
                                           "foreign(GovtAptRentModel.jibun) == BldMappingResultModel.jibun,"
                                           "foreign(GovtAptRentModel.dong) == BldMappingResultModel.dong,"
                                           "foreign(GovtAptRentModel.apt_name) == BldMappingResultModel.bld_name)")

    def to_entity_for_bld_mapping_results(self) -> GovtAptRentsEntity:
        return GovtAptRentsEntity(
            id=self.id,
            regional_cd=self.regional_cd,
            dong=self.dong,
            build_year=self.build_year,
            jibun=self.jibun,
            apt_name=self.apt_name
        )

    def to_entity_for_apt_rents(self) -> GovtAptRentsJoinKeyEntity:
        return GovtAptRentsJoinKeyEntity(
            house_id=self.bld_mapping.house_id,# if self.bld_mapping.house_id else None,  # fixme: 정상적으로 나오는지 확인 필요
            dong=self.dong,
            apt_name=self.apt_name,
            monthly_amount=self.monthly_amount,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            deposit=self.deposit,
            exclusive_area=self.exclusive_area,
            regional_cd=self.regional_cd,
            floor=self.floor
        )
