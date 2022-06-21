from sqlalchemy import Column, String, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class KaptAreaInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "kapt_area_infos"

    kapt_code = Column(String(16), primary_key=True, nullable=False)
    name = Column(String(32), nullable=True)
    kapt_tarea = Column(String(22), nullable=True)
    kapt_marea = Column(String(22), nullable=True)
    kapt_mparea_60 = Column(String(22), nullable=True)
    kapt_mparea_85 = Column(String(22), nullable=True)
    kapt_mparea_135 = Column(String(22), nullable=True)
    kapt_mparea_136 = Column(String(22), nullable=True)
    priv_area = Column(String(22), nullable=True)
    bjd_code = Column(String(10), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_kapt_area_info_entity(self) -> KaptAreaInfoEntity:
        return KaptAreaInfoEntity(
            kapt_code=self.kapt_code,
            name=self.name,
            kapt_tarea=self.kapt_tarea,
            kapt_marea=self.kapt_marea,
            kapt_mparea_60=self.kapt_mparea_60,
            kapt_mparea_85=self.kapt_mparea_85,
            kapt_mparea_135=self.kapt_mparea_135,
            kapt_mparea_136=self.kapt_mparea_136,
            priv_area=self.priv_area,
            bjd_code=self.bjd_code,
            update_needed=self.update_needed,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
