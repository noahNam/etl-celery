from typing import Any

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionInfoEntity,
    SubscriptionManualInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)


class TransformSubscription:
    def start_etl(
        self,
        target_list: list[SubscriptionInfoEntity | SubscriptionManualInfoEntity],
    ) -> dict[
        str, list[SubscriptionModel] | list[SubscriptionDetailModel] | Any
    ] | None:
        if not target_list:
            return None

        if isinstance(target_list[0], SubscriptionInfoEntity):
            return self._subscription_infos(target_list)
        elif isinstance(target_list[0], SubscriptionManualInfoEntity):
            return self._subscription_manual_infos(target_list)

    def _subscription_infos(
        self, target_list: list[SubscriptionInfoEntity]
    ) -> dict[str, list[SubscriptionModel] | list[SubscriptionDetailModel]]:
        subscriptions = list()
        subscription_details = list()
        subs_id = None

        for target_entity in target_list:

            subscription_details.append(
                SubscriptionDetailModel(
                    id=target_entity.id,
                    subs_id=target_entity.subs_id,
                    area_type=target_entity.area_type,
                    supply_price=target_entity.supply_price,
                    supply_area=target_entity.supply_area,
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
                    update_needed=target_entity.update_needed,
                )
            )

            # subscriptions은 subs_id로 묶음. 그렇지 않으면 subscription_details 만큼 obj가 생성
            if subs_id == target_entity.subs_id:
                continue

            subscriptions.append(
                SubscriptionModel(
                    subs_id=target_entity.subs_id,
                    offer_date=target_entity.offer_date,
                    notice_winner_date=target_entity.notice_winner_date,
                    name=target_entity.name,
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
                    region=target_entity.region,
                    housing_category=target_entity.housing_category,
                    rent_type=target_entity.rent_type,
                    construct_company=target_entity.construct_company,
                    contact=target_entity.contact,
                    subscription_date=target_entity.subscription_date,
                    special_supply_status=target_entity.special_supply_status,
                    cmptt_rank=target_entity.cmptt_rank,
                    update_needed=target_entity.update_needed,
                )
            )
            subs_id = target_entity.subs_id

        return dict(
            subscriptions=subscriptions, subscription_details=subscription_details
        )

    def _subscription_manual_infos(
        self, target_list: list[SubscriptionManualInfoEntity]
    ) -> dict[Any]:
        subscriptions = list()
        subscription_details = list()
        subs_id = None

        for target_entity in target_list:
            subscription_details.append(
                dict(
                    key=target_entity.id,
                    items=dict(
                        subs_id=target_entity.subs_id,
                        bay=target_entity.bay,
                        pansang_tower=target_entity.pansang_tower,
                        kitchen_window=target_entity.kitchen_window,
                        direct_window=target_entity.direct_window,
                        alpha_room=target_entity.alpha_room,
                        update_needed=target_entity.update_needed,
                    ),
                )
            )

            # subscriptions은 subs_id로 묶음. 그렇지 않으면 subscription_details 만큼 obj가 생성
            if subs_id == target_entity.subs_id:
                continue

            subscriptions.append(
                dict(
                    key=target_entity.subs_id,
                    items=dict(
                        heat_type=target_entity.heat_type,
                        vl_rat=target_entity.vl_rat,
                        bc_rat=target_entity.bc_rat,
                        hallway_type=target_entity.hallway_type,
                        hhld_total_cnt=target_entity.hhld_total_cnt,
                        park_total_cnt=target_entity.park_total_cnt,
                        highest_floor=target_entity.highest_floor,
                        dong_cnt=target_entity.dong_cnt,
                        deposit=target_entity.deposit,
                        middle_payment=target_entity.middle_payment,
                        balance=target_entity.balance,
                        restriction_sale=target_entity.restriction_sale,
                        compulsory_residence=target_entity.compulsory_residence,
                        cyber_model_house_link=target_entity.cyber_model_house_link,
                        supply_rate=target_entity.supply_rate,
                        supply_rate_etc=target_entity.supply_rate_etc,
                        update_needed=target_entity.update_needed,
                    ),
                )
            )
            subs_id = target_entity.subs_id

        return dict(
            subscriptions=subscriptions, subscription_details=subscription_details
        )
