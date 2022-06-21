from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.govt_deal_spider import (
    GovtHouseDealSpider,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.application.use_case import BaseSyncUseCase


class GovtDealUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=GovtHouseDealSpider)
        self._spider_input_params: list[LegalDongCodeEntity] = list()

    def setup(self):
        self._spider_input_params: list[LegalDongCodeEntity] = self._repo.find_all()
