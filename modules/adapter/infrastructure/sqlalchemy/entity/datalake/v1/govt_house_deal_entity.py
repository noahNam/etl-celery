from datetime import datetime

from pydantic import BaseModel


class GovtAptDealEntity(BaseModel):
    id: int
    deal_amount: int | None
    build_year: str | None
    deal_year: str | None
    road_name: str | None
    road_name_bonbun: str | None
    road_name_bubun: str | None
    road_name_sigungu_cd: str | None
    road_name_seq: str | None
    road_name_basement_cd: str | None
    road_name_cd: str | None
    dong: str | None
    bonbun_cd: str | None
    bubun_cd: str | None
    sigungu_cd: str | None
    eubmyundong_cd: str | None
    land_cd: str | None
    apt_name: str | None
    deal_month: str | None
    deal_day: str | None
    serial_no: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None
    update_needed: bool
    created_at: datetime
    updated_at: datetime


class GovtAptRentEntity(BaseModel):
    id: int
    build_year: str | None
    deal_year: str | None
    dong: str | None
    deposit: int | None
    apt_name: str | None
    deal_month: str | None
    deal_day: str | None
    monthly_amount: int | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    update_needed: bool
    created_at: datetime
    updated_at: datetime


class GovtOfctlDealEntity(BaseModel):
    id: int
    deal_amount: int | None
    deal_year: str | None
    ofctl_name: str | None
    dong: str | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None
    update_needed: bool
    created_at: datetime
    updated_at: datetime


class GovtOfctlRentEntity(BaseModel):
    id: int
    deal_year: str | None
    ofctl_name: str | None
    dong: str | None
    deposit: int | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    monthly_amount: int | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    update_needed: bool
    created_at: datetime
    updated_at: datetime


class GovtRightLotOutEntity(BaseModel):
    id: int
    deal_amount: int | None
    classification_owner_ship: str | None
    deal_year: str | None
    name: str | None
    dong: str | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    update_needed: bool
    created_at: datetime
    updated_at: datetime


class BldMappingResultEntity(BaseModel):
    id: int
    place_id: int
    house_id: int
    regional_cd: str | None
    dong: str | None
    bld_name: str | None
    created_at: datetime
    updated_at: datetime
