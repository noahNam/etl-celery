from datetime import datetime

from pydantic import BaseModel


class AptDealEntity(BaseModel):
    id: int | None
    house_id: int | None
    dong: str | None
    bld_name: str | None
    deal_amount: str | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    serial_no: str | None
    private_area: float | None
    supply_area: float | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None
    is_available: bool | None
    created_at: datetime | None
    updated_at: datetime | None


class AptRentEntity(BaseModel):
    id: int | None
    house_id: int | None
    dong: str | None
    bld_name: str | None
    monthly_amount: str | None
