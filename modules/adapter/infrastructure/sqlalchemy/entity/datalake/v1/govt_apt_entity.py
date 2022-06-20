from datetime import datetime

from pydantic import BaseModel


class GovtAptDealsEntity(BaseModel):
    id: int | None
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
    created_at: datetime | None
    updated_at: datetime | None


class GovtAptRentsEntity(BaseModel):
    id: int | None
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
    created_at: datetime | None
    updated_at: datetime | None


class GovtOfctlDealsEntity(BaseModel):
    id: int | None
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
    created_at: datetime | None
    updated_at: datetime | None


class GovtOfctlRentsEntity(BaseModel):
    id: int | None
    deal_year: str | None
    ofctl_name: str | None
    dong: str | None
    deposit: str | None
    sigungu: str | None
    deal_month: str | None
    deal_day: str | None
    monthly_amount: str | None
    exclusive_area: str | None
    jibun: str | None
    regional_cd: str | None
    floor: str | None
    created_at: str | None
    updated_at: str | None


class GovtRightLotOutsEntity(BaseModel):
    id: int | None
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
    created_at: str | None
    updated_at: str | None


class GovtTransferEntity(BaseModel):  # fixme: 명칭 변경 (수정함)
    """
    매핑테이블 전처리를 위한 임시 Entity
    TransferBldMappingResults 에서 사용.
    """
    addr_code: str | None
    build_year: str | None
    jibun: str | None
    dong: str | None
    apt_name: str | None


class GovtAptDealsJoinKeyEntity(BaseModel):
    def __init__(__pydantic_self__, **data: Any):
        super().__init__(data)
        __pydantic_self__.monthly_amount = None

    """
        govt_apt_deals 와 bld_mapping_results table의 키값을 join 함
    """
    house_id: int
    dong: str | None
    apt_name: str | None
    deal_amount: str | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    serial_no: str | None
    exclusive_area: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None


class GovtAptRentsJoinKeyEntity(BaseModel):
    house_id: int  # fixme: 매핑 안되어있으면 넘어가지 않도록 (수정함)
    dong: str | None
    apt_name: str | None
    monthly_amount: int | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    deposit: int | None
    exclusive_area: str | None
    regional_cd: str | None
    floor: str | None


class GovtOfctlDealJoinKeyEntity(BaseModel):
    house_id: int
    dong: str | None
    ofctl_name: str | None
    deal_amount: int | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    regional_cd: str | None
    floor: str | None
    cancel_deal_type: str | None
    cancel_deal_day: str | None
    req_gbn: str | None
    rdealer_lawdnm: str | None


class GovtOfctlRentJoinKeyEntity(BaseModel):
    house_id: int
    dong: str | None
    ofctl_name: str | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    deposit: int | None
    monthly_amount: int | None
    exclusive_area: str | None
    regional_cd: str | None
    floor: str | None


class GovtRightLotOutJoinKeyEntity(BaseModel):
    house_id: int
    dong: str | None
    name: str | None
    deal_amount: int | None
    classification_owner_ship: str | None
    deal_year: str | None
    deal_month: str | None
    deal_day: str | None
    exclusive_area: str | None
    regional_cd: str | None
    floor: str | None
