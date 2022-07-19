from sqlalchemy import Column, BigInteger, Integer, String, Numeric
from sqlalchemy.orm import relationship
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiAddrEntity,
)


class KakaoApiResultModel(datalake_base, TimestampMixin):
    __tablename__ = "kakao_api_results"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    x_vl = Column(Numeric(precision=11, scale=7), default=0)
    y_vl = Column(Numeric(precision=11, scale=7), default=0)
    jibun_address = Column(String(200), nullable=True)
    road_address = Column(String(200), nullable=True)
    origin_jibun_address = Column(String(200), nullable=True)
    origin_road_address = Column(String(200), nullable=True)
    bld_name = Column(String(100), nullable=True)

    def to_entity(self) -> KakaoApiResultEntity:
        return KakaoApiResultEntity(
            x_vl=self.x_vl,
            y_vl=self.y_vl,
            jibun_address=self.jibun_address,
            road_address=self.road_address,
            origin_jibun_address=self.origin_jibun_address,
            origin_road_address=self.origin_road_address,
            bld_name=self.bld_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
