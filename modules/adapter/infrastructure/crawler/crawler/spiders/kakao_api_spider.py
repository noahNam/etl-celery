from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.kakao_enum import KakaoApiEnum


class KakaoApiSpider(Spider):
    name = "kakao_place_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.KakaoApiPipeline": 300
        },
    }

    def start_requests(self):
        """self.params : list[KaptOpenApiInputEntity] from KaptOpenApiUseCase class"""

        url: str = KakaoApiEnum.KAKAO_PLACE_API_URL.value

        for param in self.params:
            yield Request(
                url=url + param.origin_dong_address,
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
                    "url": url,
                },
            )

    def parse(self, response, **kwargs):
        print(response.text)

    def error_callback_kakao_info(self, failure):
        print(failure)
