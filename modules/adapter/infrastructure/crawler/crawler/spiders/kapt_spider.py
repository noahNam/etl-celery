from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.kapt_enum import KaptEnum


class KaptSpider(Spider):
    name = "kapt_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.KaptPipeline": 300,
        },
    }

    def start_requests(self):
        urls: list = [
            KaptEnum.BASE_INFO_END_POINT.value,
            KaptEnum.DETAIL_INFO_END_POINT.value,
        ]

        yield Request(
            url=urls[0]
            + f"?kaptCode=A15876402&ServiceKey={KaptEnum.SERVICE_KEY.value}",
            callback=self.parse_kapt_base_info,
        )

        yield Request(
            url=urls[1]
            + f"?kaptCode=A15876402&ServiceKey={KaptEnum.SERVICE_KEY.value}",
            callback=self.parse_kapt_detail_info,
        )

    def parse_kapt_base_info(self, response, **kwargs):
        print("base info parse")
        print(response.text)

    def parse_kapt_detail_info(self, response, **kwargs):
        print("detail info parse")
        print(response.text)
