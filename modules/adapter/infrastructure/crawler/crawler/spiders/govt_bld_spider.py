from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.govt_bld_enum import (
    GovtBldEnum,
)
from modules.adapter.infrastructure.crawler.crawler.items import GovtBldInputInfo
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    GovtBldInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)


class GovtBldSpider(Spider):
    name = "govt_bld_infos"
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtBldPipeline": 300
    #     },
    # }
    open_api_service_key = GovtBldEnum.SERVICE_KEY_1.value
    request_count = 0

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        urls: list = [
            GovtBldEnum.GOVT_BLD_TOP_URL.value,
            GovtBldEnum.GOVT_BLD_MID_URL.value,
            GovtBldEnum.GOVT_BLD_AREA_URL.value,
        ]

        # 번지 추출
        input_params: list[GovtBldInputInfo] | None = self.get_input_infos(
            bld_info_list=self.params
        )

        if input_params:
            for param in input_params:
                yield Request(
                    url=urls[0] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_top_info,
                    errback=self.error_callback_bld_top_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )
                yield Request(
                    url=urls[1] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_mid_info,
                    errback=self.error_callback_bld_mid_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )
                yield Request(
                    url=urls[2] + f"?ServiceKey={GovtBldSpider.open_api_service_key}"
                    f"&sigunguCd={param.sigungu_code}"
                    f"&bjdongCd={param.bjdong_code}"
                    f"&platGbCd=0"
                    f"&bun={param.bun}"
                    f"&ji={param.ji}"
                    f"&numOfRows={GovtBldEnum.NUMBER_OF_ROWS.value}"
                    f"&pageNo=1",
                    callback=self.parse_bld_area_info,
                    errback=self.error_callback_bld_area_info,
                    meta={
                        "house_id": param.house_id,
                        "kapt_code": param.kapt_code,
                        "name": param.name,
                        "origin_dong_address": param.origin_dong_address,
                        "new_dong_address": param.new_dong_address,
                        "bjd_code": param.origin_bjd_code,
                        "url": urls[0]
                        + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                    },
                )

    def parse_bld_top_info(self, response, **kwargs):
        pass

    def parse_bld_mid_info(self, response, **kwargs):
        pass

    def parse_bld_area_info(self, response, **kwargs):
        pass

    def error_callback_bld_top_info(self, failure):
        pass

    def error_callback_bld_mid_info(self, failure):
        pass

    def error_callback_bld_area_info(self, failure):
        pass

    def get_input_infos(
        self, bld_info_list: list[GovtBldInputEntity]
    ) -> list[GovtBldInputInfo] | None:
        input_infos: list[GovtBldInputInfo] | None = None
        for elm in bld_info_list:
            input_infos.append(self._extract_input_params(bld_info=elm))

        return input_infos

    def _extract_input_params(self, bld_info: GovtBldInputEntity) -> GovtBldInputInfo:
        """ '0000' : 공공데이터 번지 파라미터 default value format"""
        bunji, bun, ji = None, "0000", "0000"

        if bld_info.new_dong_address:
            bunji = bld_info.new_dong_address.split(" ")[-1]
        else:
            bunji = bld_info.origin_dong_address.split(" ")[-1]

        if bunji:
            if "-" in bunji:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]
                ji = ji[len(bunji.split("-")[-1]) :] + bunji.split("-")[-1]
            else:
                bun = bun[len(bunji.split("-")[0]) :] + bunji.split("-")[0]

        return GovtBldInputInfo(
            house_id=bld_info.house_id,
            kapt_code=bld_info.kapt_code,
            name=bld_info.name,
            origin_dong_address=bld_info.origin_dong_address,
            new_dong_address=bld_info.new_dong_address,
            origin_bjd_code=bld_info.bjd_code,
            bun=bun,
            ji=ji,
            sigungu_code=bld_info.bjd_code[:5],
            bjdong_code=bld_info.bjd_code[5:],
        )

    def __save_crawling_failure(self, fail_orm: CallFailureHistoryModel) -> None:
        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )

    def __is_exists_failure(self, fail_orm: CallFailureHistoryModel | None) -> bool:
        send_message(
            topic_name=CallFailureTopicEnum.IS_EXISTS.value,
            fail_orm=fail_orm,
        )
        return event_listener_dict.get(f"{CallFailureTopicEnum.IS_EXISTS.value}")
