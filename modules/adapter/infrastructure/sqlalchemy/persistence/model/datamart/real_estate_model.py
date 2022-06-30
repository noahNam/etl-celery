from sqlalchemy import Column, String, BigInteger, Integer, Boolean, Numeric

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class RealEstateModel(datamart_base, TimestampMixin):
    __tablename__ = "real_estates"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(String(50), nullable=True)
    jibun_address = Column(String(100), nullable=True)
    road_address = Column(String(100), nullable=True)
    si_do = Column(String(20), nullable=True)
    si_gun_gu = Column(String(16), nullable=True)
    dong_myun = Column(String(16), nullable=True)
    ri = Column(String(12), nullable=True)
    road_name = Column(String(30), nullable=True)
    road_number = Column(String(10), nullable=True)
    land_number = Column(String(10), nullable=True)
    x_vl = Column(Numeric(11, 7), nullable=False)
    y_vl = Column(Numeric(11, 7), nullable=False)
    front_legal_code = Column(String(5), nullable=False, index=True)
    back_legal_code = Column(String(5), nullable=False, index=True)
    is_available = Column(Boolean, nullable=False)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            jibun_address=self.jibun_address,
            road_address=self.road_address,
            si_do=self.si_do,
            si_gun_gu=self.si_gun_gu,
            dong_myun=self.dong_myun,
            ri=self.ri,
            road_name=self.road_name,
            road_number=self.road_number,
            land_number=self.land_number,
            x_vl=self.x_vl,
            y_vl=self.y_vl,
            front_legal_code=self.front_legal_code,
            back_legal_code=self.back_legal_code,
            is_available=self.is_available,
        )
