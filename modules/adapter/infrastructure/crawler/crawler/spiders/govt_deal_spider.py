from scrapy import Spider

from modules.adapter.infrastructure.crawler.crawler.enum.govt_deal_enum import (
    GovtDealEnum,
)


class GovtHouseDealSpider(Spider):
    name = "govt_house_deal_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtHouseDealPipeline": 300
        },
    }
    open_api_service_key = GovtDealEnum.SERVICE_KEY_1.value
    request_count: int = 0


class GovtDateCounter:
    def __init__(self):
        self._min_year: int = int(GovtDealEnum.MIN_YEAR_MONTH.value.split("-")[0])
        self._min_month: int = int(GovtDealEnum.MIN_YEAR_MONTH.value.split("-")[1])
        self._max_year: int = int(GovtDealEnum.MAX_YEAR_MONTH.value.split("-")[0])
        self._max_month: int = int(GovtDealEnum.MAX_YEAR_MONTH.value.split("-")[1])
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

    def plus_month(self) -> int:
        if 0 < self._current_month < 12:
            self._current_month += 1
        else:
            self._plus_year()
            self._current_month = 1
        return self._current_month
