from scrapy import Spider, Request
from xmltodict import parse

from modules.adapter.infrastructure.crawler.crawler.enum.kapt_enum import KaptEnum
from modules.adapter.infrastructure.crawler.crawler.items import (
    KaptLocationInfoItem,
    KaptAreaInfoItem,
)


class KaptSpider(Spider):
    name = "kapt_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.KaptPipeline": 300
        },
    }
    open_api_service_key = KaptEnum.SERVICE_KEY_1.value
    request_count = 0
    change_flag = True

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        urls: list = [
            KaptEnum.BASE_INFO_END_POINT.value,
            KaptEnum.DETAIL_INFO_END_POINT.value,
        ]

        for param in self.params:
            yield Request(
                url=urls[0]
                + f"?kaptCode={param.kapt_code}&ServiceKey={KaptSpider.open_api_service_key}",
                callback=self.parse_kapt_base_info,
                errback=self.error_callback_kapt_base_info,
            )

            yield Request(
                url=urls[1]
                + f"?kaptCode={param.kapt_code}&ServiceKey={KaptSpider.open_api_service_key}",
                callback=self.parse_kapt_detail_info,
                errback=self.error_callback_kapt_detail_info,
            )

    def parse_kapt_base_info(self, response):
        xml_to_dict = parse(response.text)
        item: KaptAreaInfoItem = KaptAreaInfoItem(
            kapt_code=xml_to_dict["response"]["body"]["item"].get("kaptCode"),
            name=xml_to_dict["response"]["body"]["item"].get("kaptName"),
            kapt_tarea=xml_to_dict["response"]["body"]["item"].get("kaptTarea"),
            kapt_marea=xml_to_dict["response"]["body"]["item"].get("kaptMarea"),
            kapt_mparea_60=xml_to_dict["response"]["body"]["item"].get("kaptMparea_60"),
            kapt_mparea_85=xml_to_dict["response"]["body"]["item"].get("kaptMparea_80"),
            kapt_mparea_135=xml_to_dict["response"]["body"]["item"].get(
                "kaptMparea_135"
            ),
            kapt_mparea_136=xml_to_dict["response"]["body"]["item"].get(
                "kaptMparea_136"
            ),
            priv_area=xml_to_dict["response"]["body"]["item"].get("privArea"),
            bjd_code=xml_to_dict["response"]["body"]["item"].get("bjdCode"),
        )

        if (
                KaptSpider.request_count >= KaptEnum.DAILY_REQUEST_COUNT.value
            and KaptSpider.change_flag
        ):
            self.change_service_key()
            KaptSpider.change_flag = False
        else:
            KaptSpider.request_count += KaptSpider.request_count

        yield item

    def parse_kapt_detail_info(self, response):
        xml_to_dict = parse(response.text)
        item: KaptLocationInfoItem = KaptLocationInfoItem(
            kapt_code=xml_to_dict["response"]["body"]["item"].get("kaptCode"),
            name=xml_to_dict["response"]["body"]["item"].get("kaptName"),
            kaptd_wtimebus=xml_to_dict["response"]["body"]["item"].get("kaptdWtimebus"),
            subway_line=xml_to_dict["response"]["body"]["item"].get("subwayLine"),
            subway_station=xml_to_dict["response"]["body"]["item"].get("subwayStation"),
            kaptd_wtimesub=xml_to_dict["response"]["body"]["item"].get("kaptdWtimesub"),
            convenient_facility=xml_to_dict["response"]["body"]["item"].get(
                "convenientFacility"
            ),
            education_facility=xml_to_dict["response"]["body"]["item"].get(
                "educationFacility"
            ),
        )

        if (
                KaptSpider.request_count >= KaptEnum.DAILY_REQUEST_COUNT.value
            and KaptSpider.change_flag
        ):
            self.change_service_key()
            KaptSpider.change_flag = False
        else:
            KaptSpider.request_count += KaptSpider.request_count

        yield item

    def change_service_key(self):
        KaptSpider.open_api_service_key = KaptEnum.SERVICE_KEY_2.value

    def error_callback_kapt_base_info(self, response):
        print("base info error callback")
        print(f"-->{response}")

    def error_callback_kapt_detail_info(self, response):
        print("detail info error callback")
        print(f"-->{response}")
