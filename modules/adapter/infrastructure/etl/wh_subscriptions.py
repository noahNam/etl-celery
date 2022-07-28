from typing import Any
from tqdm import tqdm
import requests
from modules.adapter.infrastructure.crawler.crawler.enum.kakao_enum import KakaoApiEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)

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
                    place_id=target_entity.place_id,
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

    def get_kakao_address(
            self,
            subs_infos: list[SubscriptionInfoEntity],
    ) -> dict[str, list[int] | list[KakaoApiResultModel | None]]:
        # 수정이 필요한 subs_id 추출
        subs_ids = list()
        for subs_info in subs_infos:
            if not subs_info.place_id:
                subs_ids.append(subs_info.subs_id)
        subs_ids = list(set(subs_ids))

        # kakao api에 전송할 주소값 추출
        addresses = list()
        for subs_id in subs_ids:
            for subs_info in subs_infos:
                if subs_info.subs_id == subs_id:
                    if subs_info.origin_address:
                        addresses.append(subs_info.origin_address)
                    elif subs_info.new_address:
                        addresses.append(subs_info.new_address)
                    else:
                        addresses.append(None)
                    break

        # kakao api request
        kakao_addresses: list[KakaoApiResultModel | None] = list()
        kakao_key_number: int = self._get_kakao_key_usable_number()
        for i in tqdm(range(len(subs_ids)), desc="kakao_addresses", mininterval=1):
            try:
                response: KakaoApiResultModel | None = self._request_kakao_api(
                    address=addresses[i], key_number=kakao_key_number
                )
                if response in [429, 401]:
                    kakao_key_number = self._get_kakao_key_usable_number()

                    response: KakaoApiResultModel | None = self._request_kakao_api(
                        address=addresses[i], key_number=kakao_key_number
                    )
                kakao_addresses.append(response)
            except Exception as e:
                break

        return dict(subs_ids=subs_ids, kakao_addresses=kakao_addresses)

    def _get_kakao_key_usable_number(self) -> int:
        test_address = "서울 강남구 광평로10길 15"
        all_key_cnt = len(KakaoApiEnum.KAKAO_API_KEYS.value)
        key_idx = None
        for i in range(all_key_cnt):
            res = self._request_kakao_api(address=test_address, key_number=i)
            if res != 429:
                return i

        if not key_idx:
            raise Exception("kakao API limit has been exceeded")

    def filter_address(
            self,
            addr: str
    ) -> str:
        addr = addr.replace('０', '0')
        addr = addr.replace('１', '1')
        addr = addr.replace('２', '2')
        addr = addr.replace('３', '3')
        addr = addr.replace('４', '4')
        addr = addr.replace('５', '5')
        addr = addr.replace('６', '6')
        addr = addr.replace('７', '7')
        addr = addr.replace('８', '8')
        addr = addr.replace('９', '9')
        addr = addr.replace('\u3000', ' ')
        return addr

    def _request_kakao_api(
            self,
            address: str,
            key_number: int
    ) -> KakaoApiResultModel | None | int:
        address: str = self.filter_address(addr=address)

        url: str = KakaoApiEnum.KAKAO_PLACE_API_URL_NO_PARAM.value
        headers: dict = {
            "Authorization": f"KakaoAK {KakaoApiEnum.KAKAO_API_KEYS.value[key_number]}"
        }
        params = {"query": "{}".format(address)}
        res = requests.get(url=url, params=params, headers=headers)

        # kakao 응답에 문제가 있는지 확인
        if res.status_code in [429, 401]:
            return res.status_code
        else:
            kakao_addresses = res.json()["documents"]
            if not kakao_addresses:
                return None

            kakao_address = None
            for addr in kakao_addresses:
                if (
                    "아파트" in addr["category_name"]
                    and "아파트상가" not in addr["category_name"]
                ):
                    kakao_address = KakaoApiResultModel(
                        x_vl=addr["x"],
                        y_vl=addr["y"],
                        jibun_address=addr["address_name"],
                        road_address=addr["road_address_name"],
                        origin_jibun_address=address,
                        origin_road_address=None,
                        bld_name=addr["place_name"],
                    )
                    break

            return kakao_address
