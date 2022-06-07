from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.legal_code_enum import (
    LegalCodeEnum,
)


class LegalCodeSpider(Spider):
    name = "legal_code_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.LegalCodePipeline": 300
        },
    }
    open_api_service_key = LegalCodeEnum.SERVICE_KEY_1.value

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        url = LegalCodeEnum.BASE_INFO_END_POINT.value

        for i in range(LegalCodeEnum.TOTAL_PAGE_NUMBER.value):
            yield Request(
                url=url
                + f"?type=json&ServiceKey={LegalCodeSpider.open_api_service_key}&numOfRows=1000&flag=Y&pageNo={i}",
                callback=self.parse,
                errback=self.error_callback_legal_code_info,
                meta={"current_page_number": i, "url": url},
            )

    def parse(self, response, **kwargs):
        item: KakaoPlaceInfoItem | None = None
        to_json = json.loads(response.text)

    def error_callback_legal_code_info(self, failure):
        pass
