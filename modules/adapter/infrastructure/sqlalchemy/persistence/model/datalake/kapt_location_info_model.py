from sqlalchemy import Column, String

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class KaptLocationInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "kapt_location_infos"

    kapt_code = Column(String(16), primary_key=True, nullable=False)
    name = Column(String(32), nullable=True)
    kaptd_wtimebus = Column(String(10), nullable=True)
    subway_line = Column(String(50), nullable=True)
    subway_station = Column(String(50), nullable=True)
    kaptd_wtimesub = Column(String(10), nullable=True)
    convenient_facility = Column(String(500), nullable=True)
    education_facility = Column(String(500), nullable=True)
