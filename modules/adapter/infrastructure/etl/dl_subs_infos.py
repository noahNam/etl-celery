from typing import Any

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    ApplyHomeEntity,
    GoogleSheetApplyHomeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)


class TransformSubsInfo:
    def start_etl(
        self,
        from_model: str,
        target_list: list[ApplyHomeEntity | GoogleSheetApplyHomeEntity],
    ) -> list[SubscriptionInfoModel | SubscriptionManualInfoModel] | None:
        if not target_list:
            return None

        if from_model == "apply_homes":
            return self._etl_apply_homes(target_list)
        elif from_model == "google_sheet_applys":
            return self._etl_google_sheet_applys(target_list)

    def _etl_apply_homes(
        self, target_list: list[ApplyHomeEntity]
    ) -> list[SubscriptionInfoModel]:
        result = list()
        offer_date = None
        name = None
        subs_id = None

        for target_entity in target_list:
            if offer_date != target_entity.offer_date or name != target_entity.name:
                subs_id = target_entity.id

            offer_date = target_entity.offer_date
            name = target_entity.name

            result.append(
                SubscriptionInfoModel(
                    id=target_entity.id,
                    subs_id=subs_id,
                    offer_date=target_entity.offer_date,
                    notice_winner_date=target_entity.notice_winner_date,
                    name=target_entity.name,
                    area_type=target_entity.area_type,
                    supply_price=target_entity.supply_price,
                    second_subs_amount=target_entity.second_subs_amount,
                    origin_address=target_entity.origin_address,
                    new_address=target_entity.new_address,
                    supply_household=target_entity.supply_household,
                    offer_notice_url=target_entity.offer_notice_url,
                    move_in_date=target_entity.move_in_date,
                    contract_date=target_entity.contract_date,
                    hompage_url=target_entity.hompage_url,
                    special_supply_date=target_entity.special_supply_date,
                    special_supply_etc_date=target_entity.special_supply_etc_date,
                    special_etc_gyeonggi_date=target_entity.special_etc_gyeonggi_date,
                    first_supply_date=target_entity.first_supply_date,
                    first_supply_etc_date=target_entity.first_supply_etc_date,
                    first_etc_gyeonggi_date=target_entity.first_etc_gyeonggi_date,
                    second_supply_date=target_entity.second_supply_date,
                    second_supply_etc_date=target_entity.second_supply_etc_date,
                    second_etc_gyeonggi_date=target_entity.second_etc_gyeonggi_date,
                    supply_area=target_entity.supply_area,
                    region=target_entity.region,
                    housing_category=target_entity.housing_category,
                    rent_type=target_entity.rent_type,
                    construct_company=target_entity.construct_company,
                    contact=target_entity.contact,
                    subscription_date=target_entity.subscription_date,
                    special_supply_status=target_entity.special_supply_status,
                    cmptt_rank=target_entity.cmptt_rank,
                    special_household=target_entity.special_household,
                    multi_children_vol_etc_gyeonggi=target_entity.multi_children_vol_etc_gyeonggi,
                    multi_children_vol_etc=target_entity.multi_children_vol_etc,
                    multi_children_household=target_entity.multi_children_household,
                    multi_children_vol=target_entity.multi_children_vol,
                    newlywed_vol_etc_gyeonggi=target_entity.newlywed_vol_etc_gyeonggi,
                    newlywed_vol_etc=target_entity.newlywed_vol_etc,
                    newlywed_household=target_entity.newlywed_household,
                    newlywed_vol=target_entity.newlywed_vol,
                    first_life_vol_etc_gyeonggi=target_entity.first_life_vol_etc_gyeonggi,
                    first_life_vol_etc=target_entity.first_life_vol_etc,
                    first_life_household=target_entity.first_life_household,
                    first_life_vol=target_entity.first_life_vol,
                    old_parent_vol_etc_gyeonggi=target_entity.old_parent_vol_etc_gyeonggi,
                    old_parent_vol_etc=target_entity.old_parent_vol_etc,
                    old_parent_household=target_entity.old_parent_household,
                    old_parent_vol=target_entity.old_parent_vol,
                    agency_recommend_etc_gyeonggi=target_entity.agency_recommend_etc_gyeonggi,
                    agency_recommend_etc=target_entity.agency_recommend_etc,
                    agency_recommend_house_hold=target_entity.agency_recommend_house_hold,
                    agency_recommend_vol=target_entity.agency_recommend_vol,
                    official_general_household=target_entity.official_general_household,
                    general_household=target_entity.general_household,
                    first_accept_cnt=target_entity.first_accept_cnt,
                    first_accept_cnt_gyeonggi=target_entity.first_accept_cnt_gyeonggi,
                    first_accept_cnt_etc=target_entity.first_accept_cnt_etc,
                    second_accept_cnt=target_entity.second_accept_cnt,
                    second_accept_cnt_gyeonggi=target_entity.second_accept_cnt_gyeonggi,
                    second_accept_cnt_etc=target_entity.second_accept_cnt_etc,
                    first_cmptt_rate=target_entity.first_cmptt_rate,
                    first_cmptt_rate_gyeonggi=target_entity.first_cmptt_rate_gyeonggi,
                    first_cmptt_rate_etc=target_entity.first_cmptt_rate_etc,
                    second_cmptt_rate=target_entity.second_cmptt_rate,
                    second_cmptt_rate_gyeonggi=target_entity.second_cmptt_rate_gyeonggi,
                    second_cmptt_rate_etc=target_entity.second_cmptt_rate_etc,
                    lowest_win_point=target_entity.lowest_win_point,
                    lowest_win_point_gyeonggi=target_entity.lowest_win_point_gyeonggi,
                    lowest_win_point_etc=target_entity.lowest_win_point_etc,
                    top_win_point=target_entity.top_win_point,
                    top_win_point_gyeonggi=target_entity.top_win_point_gyeonggi,
                    top_win_point_etc=target_entity.top_win_point_etc,
                    avg_win_point=target_entity.avg_win_point,
                    avg_win_point_gyeonggi=target_entity.avg_win_point_gyeonggi,
                    avg_win_point_etc=target_entity.avg_win_point_etc,
                    update_needed=True,
                )
            )
        return result

    def _etl_google_sheet_applys(
        self, target_list: list[GoogleSheetApplyHomeEntity]
    ) -> list[SubscriptionManualInfoModel]:
        result = list()
        for target_entity in target_list:
            result.append(
                SubscriptionManualInfoModel(
                    id=target_entity.id,
                    subs_id=target_entity.subs_id,
                    heat_type=target_entity.heating_type,
                    vl_rat=target_entity.floor_area_ratio,
                    bc_rat=target_entity.building_cover_ratio,
                    hallway_type=target_entity.hallway_type,
                    hhld_total_cnt=target_entity.total_household,
                    park_total_cnt=target_entity.total_park_number,
                    highest_floor=target_entity.top_floor,
                    dong_cnt=target_entity.dong_number,
                    deposit=target_entity.contract_amount,
                    middle_payment=target_entity.middle_amount,
                    balance=target_entity.remain_amount,
                    restriction_sale=target_entity.sale_limit,
                    compulsory_residence=target_entity.compulsory_residence,
                    bay=target_entity.bay,
                    pansang_tower=target_entity.plate_tower_duplex,
                    kitchen_window=target_entity.kitchen_window,
                    direct_window=target_entity.cross_ventilation,
                    alpha_room=target_entity.alpha_room,
                    cyber_model_house_link=target_entity.cyber_house_link,
                    supply_rate=target_entity.cyber_house_link,
                    supply_rate_etc=target_entity.cyber_house_link,
                    update_needed=True
                )
            )
        return result
