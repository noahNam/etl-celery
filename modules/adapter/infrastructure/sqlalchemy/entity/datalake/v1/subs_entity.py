from pydantic import BaseModel


class GoogleSheetApplyHomeEntity(BaseModel):
    id: int
    subs_id: int | None
    heating_type: str | None
    floor_area_ratio: str | None
    building_cover_ratio: float | None
    hallway_type: str | None
    total_household: int | None
    total_park_number: int | None
    top_floor: int | None
    dong_number: int | None
    contract_amount: float | None
    middle_amount: float | None
    remain_amount: float | None
    sale_limit: str | None
    compulsory_residence: str | None
    bay: int | None
    plate_tower_duplex: str | None
    kitchen_window: str | None
    cross_ventilation: str | None
    alpha_room: str | None
    cyber_house_link: str | None
    supply_rate: int | None
    supply_rate_etc: int | None


class ApplyHomeEntity(BaseModel):
    id: int
    offer_date: str | None
    notice_winner_date: str | None
    name: str | None
    area_type: str | None
    supply_price: str | None
    second_subs_amount: str | None
    origin_address: str | None
    new_address: str | None
    supply_household: str | None
    offer_notice_url: str | None
    move_in_date: str | None
    contract_date: str | None
    hompage_url: str | None
    special_supply_date: str | None
    special_supply_etc_date: str | None
    special_etc_gyeonggi_date: str | None
    first_supply_date: str | None
    first_supply_etc_date: str | None
    first_etc_gyeonggi_date: str | None
    second_supply_date: str | None
    second_supply_etc_date: str | None
    second_etc_gyeonggi_date: str | None
    supply_area: str | None
    region: str | None
    housing_category: str | None
    rent_type: str | None
    construct_company: str | None
    contact: str | None
    subscription_date: str | None
    special_supply_status: str | None
    cmptt_rank: str | None
    special_household: float | None
    multi_children_vol_etc_gyeonggi: int | None
    multi_children_vol_etc: int | None
    multi_children_household: int | None
    multi_children_vol: int | None
    newlywed_vol_etc_gyeonggi: float | None
    newlywed_vol_etc: float | None
    newlywed_household: float | None
    newlywed_vol: float | None
    first_life_vol_etc_gyeonggi: float | None
    first_life_vol_etc: float | None
    first_life_household: float | None
    first_life_vol: float | None
    old_parent_vol_etc_gyeonggi: float | None
    old_parent_vol_etc: float | None
    old_parent_household: float | None
    old_parent_vol: float | None
    agency_recommend_etc_gyeonggi: str | None
    agency_recommend_etc: str | None
    agency_recommend_house_hold: str | None
    agency_recommend_vol: str | None
    official_general_household: int | None
    general_household: int | None
    first_accept_cnt: int | None
    first_accept_cnt_gyeonggi: int | None
    first_accept_cnt_etc: int | None
    second_accept_cnt: int | None
    second_accept_cnt_gyeonggi: int | None
    second_accept_cnt_etc: int | None
    first_cmptt_rate: str | None
    first_cmptt_rate_gyeonggi: str | None
    first_cmptt_rate_etc: str | None
    second_cmptt_rate: str | None
    second_cmptt_rate_gyeonggi: str | None
    second_cmptt_rate_etc: str | None
    lowest_win_point: str | None
    lowest_win_point_gyeonggi: int | None
    lowest_win_point_etc: str | None
    top_win_point: str | None
    top_win_point_gyeonggi: int | None
    top_win_point_etc: str | None
    avg_win_point: str | None
    avg_win_point_gyeonggi: float | None
    avg_win_point_etc: str | None


class SubscriptionInfoEntity(BaseModel):
    id: int
    subs_id: int | None
    offer_date: str | None
    notice_winner_date: str | None
    name: str | None
    area_type: str | None
    supply_price: str | None
    second_subs_amount: str | None
    origin_address: str | None
    new_address: str | None
    supply_household: str | None
    offer_notice_url: str | None
    move_in_date: str | None
    contract_date: str | None
    hompage_url: str | None
    special_supply_date: str | None
    special_supply_etc_date: str | None
    special_etc_gyeonggi_date: str | None
    first_supply_date: str | None
    first_supply_etc_date: str | None
    first_etc_gyeonggi_date: str | None
    second_supply_date: str | None
    second_supply_etc_date: str | None
    second_etc_gyeonggi_date: str | None
    supply_area: float | None
    region: str | None
    housing_category: str | None
    rent_type: str | None
    construct_company: str | None
    contact: str | None
    subscription_date: str | None
    special_supply_status: str | None
    cmptt_rank: str | None
    special_household: str | None
    multi_children_vol_etc_gyeonggi: str | None
    multi_children_vol_etc: str | None
    multi_children_household: str | None
    multi_children_vol: str | None
    newlywed_vol_etc_gyeonggi: str | None
    newlywed_vol_etc: str | None
    newlywed_household: str | None
    newlywed_vol: str | None
    first_life_vol_etc_gyeonggi: str | None
    first_life_vol_etc: str | None
    first_life_household: str | None
    first_life_vol: str | None
    old_parent_vol_etc_gyeonggi: str | None
    old_parent_vol_etc: str | None
    old_parent_household: str | None
    old_parent_vol: str | None
    agency_recommend_etc_gyeonggi: str | None
    agency_recommend_etc: str | None
    agency_recommend_house_hold: str | None
    agency_recommend_vol: str | None
    official_general_household: str | None
    general_household: str | None
    first_accept_cnt: str | None
    first_accept_cnt_gyeonggi: str | None
    first_accept_cnt_etc: str | None
    second_accept_cnt: str | None
    second_accept_cnt_gyeonggi: str | None
    second_accept_cnt_etc: str | None
    first_cmptt_rate: str | None
    first_cmptt_rate_gyeonggi: str | None
    first_cmptt_rate_etc: str | None
    second_cmptt_rate: str | None
    second_cmptt_rate_gyeonggi: str | None
    second_cmptt_rate_etc: str | None
    lowest_win_point: str | None
    lowest_win_point_gyeonggi: str | None
    lowest_win_point_etc: str | None
    top_win_point: str | None
    top_win_point_gyeonggi: str | None
    top_win_point_etc: str | None
    avg_win_point: str | None
    avg_win_point_gyeonggi: float | None
    avg_win_point_etc: str | None


class SubscriptionManualInfoEntity(BaseModel):
    id: int
    subs_id: int | None
    heat_type: str | None
    vl_rat: float | None
    bc_rat: float | None
    hallway_type: str | None
    hhld_total_cnt: int | None
    park_total_cnt: int | None
    highest_floor: int | None
    dong_cnt: int | None
    deposit: float | None
    middle_payment: float | None
    balance: float | None
    restriction_sale: str | None
    compulsory_residence: str | None
    bay: str | None
    pansang_tower: str | None
    kitchen_window: str | None
    direct_window: str | None
    alpha_room: str | None
    cyber_model_house_link: str | None
    supply_rate: int | None
    supply_rate_etc: int | None
