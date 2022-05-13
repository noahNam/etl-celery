from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.kapt_enum import KaptEnum


class KaptSpider(Spider):
    name = "kapt_infos"

    def start_requests(self):
        urls: list = [
            KaptEnum.BASE_INFO_END_POINT.value,
            KaptEnum.DETAIL_INFO_END_POINT.value,
        ]

        for url in urls:
            yield Request(
                url=url
                + f"?kaptCode=A15876402&ServiceKey={KaptEnum.SERVICE_KEY.value}",
                callback=self.parse,
            )

    def parse(self, response, **kwargs):
        print(response.text)
