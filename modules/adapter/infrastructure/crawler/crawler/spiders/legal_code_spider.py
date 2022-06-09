import json

from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.legal_code_enum import (
    LegalCodeEnum,
)
from modules.adapter.infrastructure.crawler.crawler.items import LegalDongCodeItem
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
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

        for i in range(1, LegalCodeEnum.TOTAL_PAGE_NUMBER.value + 1):
            yield Request(
                url=url
                + f"?type=json&ServiceKey={LegalCodeSpider.open_api_service_key}&numOfRows=1000&flag=Y&pageNo={i}",
                callback=self.parse,
                errback=self.error_callback_legal_code_info,
                meta={"current_page_number": i, "url": url},
            )

    def parse(self, response, **kwargs):
        to_json = json.loads(response.text)

        for elm in to_json["StanReginCd"][1]["row"]:
            item: LegalDongCodeItem | None = LegalDongCodeItem(
                region_cd=elm["region_cd"],
                sido_cd=elm["sido_cd"],
                sgg_cd=elm["sgg_cd"],
                umd_cd=elm["umd_cd"],
                ri_cd=elm["ri_cd"],
                locatjumin_cd=elm["locatjumin_cd"],
                locatjijuk_cd=elm["locatjijuk_cd"],
                locatadd_nm=elm["locatadd_nm"],
                locat_order=elm["locat_order"],
                locat_rm=elm["locat_rm"],
                locathigh_cd=elm["locathigh_cd"],
                locallow_nm=elm["locallow_nm"],
                adpt_de=elm["adpt_de"],
            )

            if item:
                yield item
            else:
                current_url = response.request.meta["url"]
                current_page = response.request.meta["current_page_number"]
                self.save_failure_info(
                    current_page=current_page,
                    current_url=current_url,
                    response=response,
                )

    def error_callback_legal_code_info(self, failure):
        current_url = failure.request.meta["url"]
        current_page = failure.request.meta["current_page_number"]

        self.save_failure_info(
            current_page=current_page, current_url=current_url, response=failure
        )

    def save_failure_info(
        self,
        current_page,
        current_url,
        response,
    ) -> None:
        fail_orm = CallFailureHistoryModel(
            ref_id=None,
            ref_table="legal_dong_codes",
            param=f"url: {current_url}, " f"current_page: {current_page}",
            reason=f"response:{response.value}",
        )

        self.__save_crawling_failure(fail_orm=fail_orm)

    def __save_crawling_failure(self, fail_orm) -> None:
        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )
