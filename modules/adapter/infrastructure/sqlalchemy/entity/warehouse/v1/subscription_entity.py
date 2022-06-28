from pydantic import BaseModel


class SubsToPublicEntity(BaseModel):
    subs_id: int
    place_id: int
    name: str
    region: str
    housing_category: str
    rent_type: str
    # trade_type 데이터가 없음
    construct_company: str | None
    supply_household: str
    offer_date: str | None
    subscription_date: str | None
    special_supply_date: str | None
    special_supply_etc_date: str | None
    special_etc_gyeonggi_date: str | None
    first_supply_date: str | None
    first_supply_etc_date: str | None
    first_etc_gyeonggi_date: str | None
    second_supply_date: str | None
    second_supply_etc_date: str | None
    second_etc_gyeonggi_date: str | None
    notice_winner_date: str | None
    contract_date: str
    move_in_date: str
    min_down_payment: int | None
    max_down_payment: int | None
    supply_price: str | None
    cyber_model_house_link: str | None
    hompage_url: str | None
    offer_notice_url: str | None
    heat_type: str | None
    vl_rat: str | None
    bc_rat: str | None
    hhld_total_cnt: str | None
    park_total_cnt: str | None
    highest_floor: str | None
    dong_cnt: str | None
    deposit: float | None
    middle_payment: float | None
    balance: float | None
    restriction_sale: str | None
    compulsory_residence: str | None
    hallway_type: str | None


class SubDtToPublicDtEntity(BaseModel):
    id: int
    subs_id: int
    area_type: str | None
    supply_area: float | None
    supply_price: str
    special_household: str
    multi_children_household: str
    newlywed_household: str
    old_parent_household: str
    first_life_household: str
    general_household: str
    bay: str | None
    pansang_tower: str | None
    kitchen_window: str | None
    direct_window: str | None
    alpha_room: str | None
    cyber_model_house_link: str | None
    housing_category: str
    region: str
    supply_rate: float | None
    supply_rate_etc: float | None
    multi_children_vol: str | None
    multi_children_vol_etc_gyeonggi: str | None
    multi_children_vol_etc: str | None
    newlywed_vol: str | None
    newlywed_vol_etc_gyeonggi: str | None
    newlywed_vol_etc: str | None
    old_parent_vol: str | None
    old_parent_vol_etc_gyeonggi: str | None
    old_parent_vol_etc: str | None
    first_life_vol: str | None
    first_life_vol_etc_gyeonggi: str | None
    first_life_vol_etc: str | None
    first_accept_cnt: str | None
    first_accept_cnt_gyeonggi: str | None
    first_accept_cnt_etc: str | None
    first_cmptt_rate: str | None
    first_cmptt_rate_gyeonggi: str | None
    first_cmptt_rate_etc: str | None
    lowest_win_point: str | None
    lowest_win_point_gyeonggi: str | None
    lowest_win_point_etc: str | None
