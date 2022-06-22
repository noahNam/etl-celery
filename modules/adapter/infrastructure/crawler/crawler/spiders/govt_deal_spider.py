from scrapy import Spider, Request

from modules.adapter.infrastructure.crawler.crawler.enum.govt_deal_enum import (
    GovtHouseDealEnum,
)
from modules.adapter.infrastructure.crawler.crawler.items import GovtHouseDealInputInfo
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)


class GovtDateCounter:
    def __init__(self):
        self._min_year: int = int(GovtHouseDealEnum.MIN_YEAR_MONTH.value.split("-")[0])
        self._min_month: int = int(GovtHouseDealEnum.MIN_YEAR_MONTH.value.split("-")[1])
        self._max_year: int = int(GovtHouseDealEnum.MAX_YEAR_MONTH.value.split("-")[0])
        self._max_month: int = int(GovtHouseDealEnum.MAX_YEAR_MONTH.value.split("-")[1])
        self._current_year: int = self._min_year
        self._current_month: int = self._min_month

    def current_ym(self) -> str:
        if 0 < self._current_month < 10:
            return str(self._current_year) + "0" + str(self._current_month)
        else:
            return str(self._current_year) + str(self._current_month)

    def _is_countable_year(self) -> bool:
        if self._current_year >= self._max_year:
            return False
        return True

    def _is_countable_month(self) -> bool:
        if not self._is_countable_year() and self._current_month < self._max_month:
            return True
        if self._is_countable_year() and self._current_month < 12:
            return True
        return False

    def _plus_year(self) -> int:
        self._current_year += 1
        return self._current_year

    def plus_month(self) -> str:
        if 0 < self._current_month < 12:
            self._current_month += 1
        else:
            self._plus_year()
            self._current_month = 1
        return self.current_ym()

    def reset_counter(self) -> None:
        self._current_year: int = self._min_year
        self._current_month: int = self._min_month

    def get_max_ym(self) -> str:
        if 0 < self._max_month < 10:
            return str(self._max_year) + "0" + str(self._max_month)
        else:
            return str(self._max_year) + str(self._max_month)


class GovtHouseDealSpider(Spider):
    name = "govt_house_deal_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtHouseDealPipeline": 300
        },
    }
    open_api_service_key = GovtHouseDealEnum.SERVICE_KEY_1.value
    request_count: int = 0
    date_counter: GovtDateCounter = GovtDateCounter()

    def start_requests(self):
        """self.params: list[LegalDongCodeEntity] from GovtDealUseCase class"""
        urls: list = [
            GovtHouseDealEnum.APT_DEAL_END_POINT.value,
            GovtHouseDealEnum.APT_RENT_END_POINT.value,
            GovtHouseDealEnum.OPCTL_DEAL_END_POINT.value,
            GovtHouseDealEnum.OPCTL_RENT_END_POINT.value,
            GovtHouseDealEnum.APT_RIGHT_LOT_OUT_END_POINT.value,
        ]

        # 법정동 코드 앞 5자리 추출
        input_params: list[GovtHouseDealInputInfo] | None = self.get_input_infos(
            deal_info_list=self.params
        )

        if input_params:
            # param: 추출된 법정동 코드 앞 5자리(277개)
            for param in input_params:
                # current_ym: 200601 ~ 202206 (기간 조정시 GovtHouseDealEnum 값 조정)
                while (
                    GovtHouseDealSpider.date_counter.current_ym()
                    <= GovtHouseDealSpider.date_counter.get_max_ym()
                ):
                    yield Request(
                        url=urls[0]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_apt_deal_info,
                        errback=self.error_callback_apt_deal_info,
                        meta={
                            "url": urls[0],
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    GovtHouseDealSpider.date_counter.plus_month()
                GovtHouseDealSpider.date_counter.reset_counter()

    def parse_apt_deal_info(self):
        pass

    def parse_apt_rent_info(self):
        pass

    def parse_opctl_deal_info(self):
        pass

    def parse_opctl_rent_info(self):
        pass

    def parse_apt_right_lot_out_info(self):
        pass

    def error_callback_apt_deal_info(self):
        pass

    def error_callback_apt_rent_info(self):
        pass

    def error_callback_opctl_deal_info(self):
        pass

    def error_callback_opctl_rent_info(self):
        pass

    def error_callback_apt_right_lot_out_info(self):
        pass

    def get_input_infos(
        self, deal_info_list: list[LegalDongCodeEntity]
    ) -> list[GovtHouseDealInputInfo]:
        extracted: list[str] = list()
        for info in deal_info_list:
            extracted.append(info.region_cd[:5])

        # 중복 제거
        duplication_removed: list[str] = list(set(extracted))

        result: list[GovtHouseDealInputInfo] = list()

        for elm in duplication_removed:
            result.append(GovtHouseDealInputInfo(bjd_front_code=elm))

        return result

    def change_service_key(self):
        if (
            GovtHouseDealSpider.open_api_service_key
            == GovtHouseDealEnum.SERVICE_KEY_2.value
        ):
            GovtHouseDealSpider.open_api_service_key = (
                GovtHouseDealEnum.SERVICE_KEY_1.value
            )
        else:
            GovtHouseDealSpider.open_api_service_key = (
                GovtHouseDealEnum.SERVICE_KEY_2.value
            )

    def count_requests(self):
        if (
            GovtHouseDealSpider.request_count
            >= GovtHouseDealEnum.DAILY_REQUEST_COUNT.value
        ):
            self.change_service_key()
            GovtHouseDealSpider.request_count = 0
        else:
            GovtHouseDealSpider.request_count += 1

    def save_failure_info(self):
        pass

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
