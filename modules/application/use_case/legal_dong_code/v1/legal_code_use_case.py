from scrapy.crawler import Crawler

from modules.adapter.infrastructure.sqlalchemy.entity.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.application.use_case import BaseSyncUseCase


class LegalCodeUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=LegalCodeSpider)
        self._spider_input_params: list[LegalDongCodeEntity] = list()

    def setup(self):
        pass
