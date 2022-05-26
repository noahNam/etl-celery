from sqlalchemy import Column, String

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
