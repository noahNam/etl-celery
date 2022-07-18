from pydantic import BaseModel


class AptDealEntity(BaseModel):
    id: int
    house_id: int
    dong: str | None
    bld_name: str | None
    deal_amount: int
    deal_year: str
    deal_month: str
    deal_day: str
    serial_no: str | None
    private_area: float
    supply_area: float | None
    regional_cd: str
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None
    is_available: bool
    update_needed: bool


class AptRentEntity(BaseModel):
    id: int
    house_id: int
    dong: str | None
    bld_name: str | None
    monthly_amount: int
    deal_year: str
    deal_month: str
    deal_day: str
    deposit: int | None
    private_area: float | None
    supply_area: float | None
    regional_cd: str
    floor: str | None
    is_available: bool
    update_needed: bool


class OfctlDealEntity(BaseModel):
    id: int
    house_id: int
    dong: str | None
    bld_name: str | None
    deal_amount: int
    deal_year: str
    deal_month: str
    deal_day: str
    private_area: float | None
    supply_area: float | None
    regional_cd: str
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None
    is_available: bool
    update_needed: bool


class OfctlRentEntity(BaseModel):
    id: int
    house_id: int
    dong: str | None
    bld_name: str | None
    deal_year: str
    deal_month: str
    deal_day: str
    deposit: int | None
    monthly_amount: int
    private_area: float | None
    supply_area: float | None
    regional_cd: str
    floor: str | None
    is_available: bool
    update_needed: bool


class RightLotOutEntity(BaseModel):
    id: int
    house_id: int
    dong: str | None
    bld_name: str | None
    deal_amount: int
    classification_owner_ship: str | None
    deal_year: str
    deal_month: str
    deal_day: str
    private_area: float | None
    supply_area: float | None
    regional_cd: str
    floor: str | None
    is_available: bool
    update_needed: bool
