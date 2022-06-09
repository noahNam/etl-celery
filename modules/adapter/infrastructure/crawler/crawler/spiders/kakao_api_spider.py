import json
from http import HTTPStatus

import requests
from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.kakao_enum import KakaoApiEnum
from modules.adapter.infrastructure.crawler.crawler.items import KakaoPlaceInfoItem
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.kakao_api_enum import (
    KakaoApiTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)


class KakaoApiSpider(Spider):
    name = "kakao_place_infos"

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        url: str = KakaoApiEnum.KAKAO_PLACE_API_URL.value

        for param in self.params:
            yield Request(
                url=url + param.new_dong_address
                if param.new_dong_address
                else url + param.origin_dong_address,
                headers={
                    "Authorization": f"KakaoAK {KakaoApiEnum.KAKAO_API_KEY.value}"
                },
                callback=self.parse,
                errback=self.error_callback_kakao_info,
                meta={
                    "house_id": param.house_id,
                    "kapt_code": param.kapt_code,
                    "name": param.name,
                    "origin_dong_address": param.origin_dong_address,
                    "origin_road_address": param.origin_road_address,
                    "new_dong_address": param.new_dong_address,
                    "new_road_address": param.new_road_address,
                    "url": url,
                },
            )

    def parse(self, response, **kwargs):
        item: KakaoPlaceInfoItem | None = None
        to_json = json.loads(response.text)

        for result in to_json["documents"]:
            if (
                "아파트" in result["category_name"]
                and "아파트상가" not in result["category_name"]
            ):
                item: KakaoPlaceInfoItem | None = self.get_kakao_info_item(
                    x=result["x"],
                    y=result["y"],
                    jibun_address=result["address_name"],
                    road_address=result["road_address_name"],
                    place_name=result["place_name"],
                )
            break

        # retry 2 times
        if not item:
            keywords: list[str] = [
                response.request.meta["new_road_address"]
                if response.request.meta.get("new_road_address")
                else response.request.meta["origin_road_address"],
                response.request.meta["name"],
            ]

            for keyword in keywords:
                item = self.retry_kakao_infos(keyword=keyword)

                if item:
                    break

        if item:
            # yield item
            new_model: KakaoApiResultModel = KakaoApiResultModel(
                x_vl=item.x_vl,
                y_vl=item.y_vl,
                jibun_address=item.jibun_address,
                road_address=item.road_address,
                origin_jibun_address=response.request.meta["origin_dong_address"],
                origin_road_address=response.request.meta["origin_road_address"],
                bld_name=item.bld_name,
            )
            # 중복 저장 제거
            if not self.__is_exists_by_origin_address(kakao_orm=new_model):
                place_id = self.__save_kakao_infos(kakao_orm=new_model)
                self.update_kapt_place_id(
                    house_id=response.request.meta["house_id"], place_id=place_id
                )

        else:
            # 못 찾았거나 잘못 찾은 경우
            self.save_failure_info(
                current_house_id=response.request.meta["house_id"],
                current_kapt_code=response.request.meta["kapt_code"],
                current_bld_name=response.request.meta["name"],
                new_dong_address=response.request.meta["new_dong_address"],
                new_road_address=response.request.meta["new_road_address"],
                origin_dong_address=response.request.meta["origin_dong_address"],
                origin_road_address=response.request.meta["origin_road_address"],
                current_url=response.request.meta["url"],
                response=response,
            )

    def error_callback_kakao_info(self, failure):
        self.save_failure_info(
            current_house_id=failure.request.meta["house_id"],
            current_kapt_code=failure.request.meta["kapt_code"],
            current_bld_name=failure.request.meta["name"],
            new_dong_address=failure.request.meta["new_dong_address"],
            new_road_address=failure.request.meta["new_road_address"],
            origin_dong_address=failure.request.meta["origin_dong_address"],
            origin_road_address=failure.request.meta["origin_road_address"],
            current_url=failure.request.meta["url"],
            response=failure,
        )

    def get_kakao_info_item(
        self, x: float, y: float, jibun_address: str, road_address: str, place_name: str
    ) -> KakaoPlaceInfoItem | None:
        if not x or not y or not jibun_address or not road_address or not place_name:
            return None

        return KakaoPlaceInfoItem(
            x_vl=x,
            y_vl=y,
            jibun_address=jibun_address,
            road_address=road_address,
            bld_name=place_name,
        )

    def retry_kakao_infos(self, keyword: str | None) -> KakaoPlaceInfoItem | None:
        response = requests.get(
            url=KakaoApiEnum.KAKAO_PLACE_API_URL.value + keyword,
            headers={"Authorization": f"KakaoAK {KakaoApiEnum.KAKAO_API_KEY.value}"},
        )

        if response.status_code == HTTPStatus.OK:
            to_json = json.loads(response.text)
            for result in to_json["documents"]:
                if (
                    "아파트" in result["category_name"]
                    and "아파트상가" not in result["category_name"]
                ):
                    return self.get_kakao_info_item(
                        x=result["x"],
                        y=result["y"],
                        jibun_address=result["address_name"],
                        road_address=result["road_address_name"],
                        place_name=result["place_name"],
                    )

        return None

    def save_failure_info(
        self,
        current_house_id,
        current_kapt_code,
        current_bld_name,
        new_dong_address,
        new_road_address,
        origin_dong_address,
        origin_road_address,
        current_url,
        response,
    ) -> None:
        fail_orm = CallFailureHistoryModel(
            ref_id=current_house_id,
            ref_table="kakao_api_results",
            param=f"url: {current_url}, "
            f"kapt_code: {current_kapt_code}, "
            f"current_bld_name: {current_bld_name}, "
            f"origin_dong_address: {origin_dong_address}, "
            f"origin_road_address: {origin_road_address}, "
            f"new_dong_address: {new_dong_address}, "
            f"new_road_address: {new_road_address}",
            reason=f"response:{response.text}",
        )

        self.__save_crawling_failure(fail_orm=fail_orm)

    def update_kapt_place_id(self, house_id: int, place_id: int):
        self.repo.update_place_id(house_id=house_id, place_id=place_id)

    def __save_crawling_failure(self, fail_orm) -> None:
        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )

    def __save_kakao_infos(self, kakao_orm: KakaoApiResultModel) -> int | None:
        send_message(
            topic_name=KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value,
            kakao_orm=kakao_orm,
        )
        return event_listener_dict.get(
            f"{KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}"
        )

    def __is_exists_by_origin_address(
        self, kakao_orm: KakaoApiResultModel
    ) -> int | None:
        send_message(
            topic_name=KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value,
            kakao_orm=kakao_orm,
        )
        return event_listener_dict.get(
            f"{KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value}"
        )
