import json

from itemadapter import ItemAdapter
from scrapy import Spider, Request
from xmltodict import parse

from modules.adapter.infrastructure.crawler.crawler.enum.kapt_enum import KaptEnum
from modules.adapter.infrastructure.crawler.crawler.items import KaptBasisInfoItem


class KaptSpider(Spider):
    name = "kapt_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.KaptPipeline": 300,
        },
    }

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        urls: list = [
            KaptEnum.BASE_INFO_END_POINT.value,
            KaptEnum.DETAIL_INFO_END_POINT.value,
        ]

        for param in self.params:
            yield Request(
                url=urls[0]
                + f"?kaptCode={param.kapt_code}&ServiceKey={KaptEnum.SERVICE_KEY.value}",
                callback=self.parse_kapt_base_info,
                errback=self.error_callback_kapt_base_info,
            )

            yield Request(
                url=urls[1]
                + f"?kaptCode={param.kapt_code}&ServiceKey={KaptEnum.SERVICE_KEY.value}",
                callback=self.parse_kapt_detail_info,
                errback=self.error_callback_kapt_detail_info,
            )

    def parse_kapt_base_info(self, response, **kwargs):
        xml_to_dict = parse(response.text)
        item: KaptBasisInfoItem = KaptBasisInfoItem(
            url=response.url,
            kapt_code=xml_to_dict["response"]["body"]["item"].get("kaptCode"),
            kapt_name=xml_to_dict["response"]["body"]["item"].get("kaptName"),
            kapt_addr=xml_to_dict["response"]["body"]["item"].get("kaptAddr"),
        )
        yield item

    def parse_kapt_detail_info(self, response, **kwargs):
        print("detail info parse")
        print(response.text)

    def error_callback_kapt_base_info(self, response, **kwargs):
        print("base info error callback")
        print(f"-->{response}")

    def error_callback_kapt_detail_info(self, response, **kwargs):
        print("detail info error callback")
        print(f"-->{response}")
