from sqlalchemy import Column, String, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptLocationInfoEntity,
)
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
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_kapt_location_info_entity(self) -> KaptLocationInfoEntity:
        return KaptLocationInfoEntity(
            kapt_code=self.kapt_code,
            name=self.name,
            kaptd_wtimebus=self.kaptd_wtimebus,
            subway_line=self.subway_line,
            subway_station=self.subway_station,
            kaptd_wtimesub=self.kaptd_wtimesub,
            convenient_facility=self.convenient_facility,
            education_facility=self.education_facility,
            update_needed=self.update_needed,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
