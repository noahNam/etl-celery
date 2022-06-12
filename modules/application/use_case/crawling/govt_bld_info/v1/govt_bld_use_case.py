from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.govt_bld_spider import (
    GovtBldSpider,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    GovtBldInputEntity,
)

from modules.application.use_case import BaseSyncUseCase


class GovtBldUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=GovtBldSpider)
        self._spider_input_params: list[GovtBldInputEntity] = list()

    def setup(self):
        self._spider_input_params: list[
            GovtBldInputEntity
        ] = self._repo.find_all_bld_infos()
