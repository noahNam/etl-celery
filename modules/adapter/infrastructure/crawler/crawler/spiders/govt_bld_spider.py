from scrapy import Spider

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
