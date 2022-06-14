from datetime import datetime

from pydantic import BaseModel


class BldMappingResultsEntity(BaseModel):
    place_id: int
    house_id: int
    regional_cd: str | None
    jibun: str | None
    dong: str | None
    bld_name: str | None
    created_at: str | datetime
    updated_at: str | datetime
