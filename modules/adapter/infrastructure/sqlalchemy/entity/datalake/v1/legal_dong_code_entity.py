from datetime import datetime

from pydantic import BaseModel


class LegalDongCodeEntity(BaseModel):
    id: int
    region_cd: str | None
    sido_cd: str | None
    sgg_cd: str | None
    umd_cd: str | None
    ri_cd: str | None
    locatjumin_cd: str | None
    locatjijuk_cd: str | None
    locatadd_nm: str | None
    locat_order: str | None
    locat_rm: str | None
    locathigh_cd: str | None
    locallow_nm: str | None
    adpt_de: str | None
    created_at: datetime
    updated_at: datetime
