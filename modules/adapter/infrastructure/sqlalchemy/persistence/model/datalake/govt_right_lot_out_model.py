from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtRightLotOutsEntity,
    GovtRightLotOutJoinKeyEntity
)


class GovtRightLotOutModel(datalake_base, TimestampMixin):
    __tablename__ = "govt_right_lot_outs"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    deal_amount = Column(Integer, nullable=True)
    classification_owner_ship = Column(String(2), nullable=True)
    deal_year = Column(String(4), nullable=True)
    name = Column(String(40), nullable=True)
    dong = Column(String(40), nullable=True)
    sigungu = Column(String(40), nullable=True)
    deal_month = Column(String(2), nullable=True)
    deal_day = Column(String(6), nullable=True)
    exclusive_area = Column(String(20), nullable=True)
    jibun = Column(String(10), nullable=True)
    regional_cd = Column(String(5), nullable=True, index=True)
    floor = Column(String(4), nullable=True)

    bld_mapping = relationship("BldMappingResultModel",
                               backref="govt_right_lot_outs", uselist=False,
                               primaryjoin="and_(foreign(GovtRightLotOutModel.regional_cd) == BldMappingResultModel.regional_cd,"
                                           "foreign(GovtRightLotOutModel.jibun) == BldMappingResultModel.jibun,"
                                           "foreign(GovtRightLotOutModel.dong) == BldMappingResultModel.dong,"
                                           "foreign(GovtRightLotOutModel.name) == BldMappingResultModel.bld_name)"
                               )

    # GovtRightLotOutsEntity
    def to_entity_for_bld_mapping_results(self) -> GovtRightLotOutsEntity:
        return GovtRightLotOutsEntity(
            id=self.id,
            regional_cd=self.regional_cd,
            dong=self.dong,
            jibun=self.jibun,
            name=self.name
        )

    def to_entity_for_right_lot_outs(self) -> GovtRightLotOutJoinKeyEntity:
        return GovtRightLotOutJoinKeyEntity(
            house_id=self.bld_mapping.house_id,
            dong=self.dong,
            name=self.name,
            deal_amount=self.deal_amount,
            classification_owner_ship=self.classification_owner_ship,
            deal_year=self.deal_year,
            deal_month=self.deal_month,
            deal_day=self.deal_day,
            exclusive_area=self.exclusive_area,
            regional_cd=self.regional_cd,
            floor=self.floor,
        )
