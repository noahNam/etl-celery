from pydantic import BaseModel


class SubsToPublicEntity(BaseModel):
    subs_id: int
    name: str
    region: str
    housing_category: str
    rent_type: str
    # trade_type ??
    construct_company: str | None
    supply_household: str  #fixme: 자료형이 int가 아닐까
    offer_date: str | None
    subscription_date: str | None  # 청약기간
    special_supply_date: str | None  # 특별공급 공급이 없을 수 있음
    special_supply_etc_date: str | None
    special_etc_gyeonggi_date: str | None
    first_supply_date: str | None
    first_supply_etc_date: str | None
    first_etc_gyeonggi_date: str | None
    second_supply_date: str | None  # 2순위 공급이 없을 수 있음
    second_supply_etc_date: str | None
    second_etc_gyeonggi_date: str | None
    notice_winner_date: str | None
    contract_date: str  # 계약 시작일, 종료일
    move_in_date: str  # 입주 년, 월
    min_down_payment: int | None
    max_down_payment: int | None
    # deposit: float  # 계약금 퍼센트
    supply_price: str | None  # subscription_details 에 있음 ???
    cyber_model_house_link: str | None  # fixme: 이게 맞는지??
    offer_notice_url: str | None
    heat_type: str | None
    vl_rat: str | None
    bc_rat: str | None
    hhld_total_cnt: str | None
    park_total_cnt: str | None
    highest_floor: str | None
    dong_cnt: str | None
    deposit: float | None  # 계약금 퍼센트
    middle_payment: float | None  # 중도금
    balance: float | None  # 잔금
    restriction_sale: str | None  # 전매제한
    compulsory_residence: str | None  # 의무거주
    hallway_type: str | None  # 복도유형










