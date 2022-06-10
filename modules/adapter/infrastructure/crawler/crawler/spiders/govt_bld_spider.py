from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.govt_bld_enum import (
    GovtBldEnum,
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

        for param in self.params:
            yield Request(
                url=urls[0]
                + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                callback=self.parse_bld_top_info,
                errback=self.error_callback_bld_top_info,
                meta={
                    "house_id": param.house_id,
                    "kapt_code": param.kapt_code,
                    "name": param.name,
                    "origin_dong_address": param.origin_dong_address,
                    "new_dong_address": param.new_dong_address,
                    "bjd_code": param.bjd_code,
                    "url": urls[0]
                    + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                },
            )
            yield Request(
                url=urls[1]
                + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                callback=self.parse_bld_mid_info,
                errback=self.error_callback_bld_mid_info,
                meta={
                    "house_id": param.house_id,
                    "kapt_code": param.kapt_code,
                    "name": param.name,
                    "origin_dong_address": param.origin_dong_address,
                    "new_dong_address": param.new_dong_address,
                    "bjd_code": param.bjd_code,
                    "url": urls[0]
                    + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                },
            )
            yield Request(
                url=urls[2]
                + f"?kaptCode={param.kapt_code}&ServiceKey={GovtBldSpider.open_api_service_key}",
                callback=self.parse_bld_area_info,
                errback=self.error_callback_bld_area_info,
                meta={
                    "house_id": param.house_id,
                    "kapt_code": param.kapt_code,
                    "name": param.name,
                    "origin_dong_address": param.origin_dong_address,
                    "new_dong_address": param.new_dong_address,
                    "bjd_code": param.bjd_code,
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
