from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
    GovtAptDealsJoinKeyEntity
)


class GovtAptDealModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_apt_deals"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_amount = Column(Integer, nullable=True)
    build_year = Column(String(4), nullable=True)
    deal_year = Column(String(4), nullable=True)
    road_name = Column(String(40), nullable=True)
    road_name_bonbun = Column(String(5), nullable=True)
    road_name_bubun = Column(String(5), nullable=True)
    road_name_sigungu_cd = Column(String(5), nullable=True)
    road_name_seq = Column(String(2), nullable=True)
    road_name_basement_cd = Column(String(1), nullable=True)
    road_name_cd = Column(String(7), nullable=True)
    dong = Column(String(40), nullable=True)
    bonbun_cd = Column(String(4), nullable=True)
    bubun_cd = Column(String(4), nullable=True)
    sigungu_cd = Column(String(5), nullable=True)
    eubmyundong_cd = Column(String(5), nullable=True)
    land_cd = Column(String(1), nullable=True)
    apt_name = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    serial_no = Column(String(14), nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)
    cancel_deal_type = Column(String(1), nullable=True)
    cancel_deal_day = Column(String(8), nullable=True)
    req_gbn = Column(String(10), nullable=True)
    rdealer_lawdnm = Column(String(150), nullable=True)

    bld_mapping = relationship("BldMappingResultModel",
                               backref="govt_apt_deals",
                               primaryjoin="and_(foreign(GovtAptDealModel.regional_cd) == BldMappingResultModel.regional_cd,"
                                           "foreign(GovtAptDealModel.jibun) == BldMappingResultModel.jibun,"
                                           "foreign(GovtAptDealModel.dong) == BldMappingResultModel.dong,"
                                           "foreign(GovtAptDealModel.apt_name) == BldMappingResultModel.bld_name)",
                               uselist=False)

    def to_entity_for_bld_mapping_reuslts(self) -> GovtAptDealsEntity:
        return GovtAptDealsEntity(
            id=self.id,
            sigungu_cd=self.sigungu_cd,
            eubmyundong_cd=self.eubmyundong_cd,
            build_year=self.build_year,
            jibun=self.jibun,
            apt_name=self.apt_name,
            dong=self.dong
        )

    def to_entity_for_apt_deals(self) -> GovtAptDealsJoinKeyEntity:
        return GovtAptDealsJoinKeyEntity(
            house_id=self.bld_mapping.house_id,  # fixme: 정상적으로 나오는지 확인 필요
            dong=self.dong,
            apt_name=self.apt_name,
            deal_amount=self.deal_amount,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            serial_no=self.serial_no,
            exclusive_area=self.exclusive_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
            cancel_deal_type=self.cancel_deal_type,
            cancel_deal_day=self.cancel_deal_day,
            req_gbn=self.req_gbn,
            rdealer_lawdnm=self.rdealer_lawdnm
        )
