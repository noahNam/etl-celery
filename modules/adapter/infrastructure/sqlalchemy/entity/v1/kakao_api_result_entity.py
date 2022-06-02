from datetime import datetime

from pydantic import BaseModel


class KakaoApiResultEntity(BaseModel):
    x_vl: float
    y_vl: float
    road_address: str | None
    jibun_address: str | None
    bld_name: str | None
    created_at: datetime
    updated_at: datetime
