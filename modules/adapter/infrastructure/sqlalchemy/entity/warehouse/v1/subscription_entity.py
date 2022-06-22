from pydantic import BaseModel


class SubsToPublicEntity(BaseModel):
    name: str
    region: str
    housing_category: str
    rent_type: str
    # trade_type ??
    construct_company: str
    supply_household: float  #fixme: 자료형이 int가 아닐까
    offer_date: str
    subscription_date: str  # 청약기간
    special_supply_date: str | None  # 특별공급 공급이 없을 수 있음
    special_supply_etc_date: str | None
    special_etc_gyeonggi_date: str | None
    first_supply_date: str
    first_supply_etc_date: str
    first_etc_gyeonggi_date: str | None
    second_supply_date: str | None  # 2순위 공급이 없을 수 있음
    second_supply_etc_date: str | None
    second_etc_gyeonggi_date: str | None
    notice_winner_date: str
    contract_date: str  # 계약 시작일, 종료일
    move_in_date: str  # 입주 년, 월
    # deposit: float  # 계약금 퍼센트
    supply_price: str  # subscription_details 에 있음
    cyber_model_house_link: str  # fixme: 이게 맞는지??
    offer_notice_url: str
    heat_type: str
    vl_rat: str
    bc_rat: str
    hhld_total_cnt: str
    park_total_cnt: str
    highest_floor: str
    dong_cnt: str
    deposit: float  # 계약금 퍼센트
    middle_payment: float  # 중도금
    balance: float  # 잔금
    restriction_sale: str  # 전매제한
    compulsory_residence: str  # 의무거주
    hallway_type: str  # 복도유형










