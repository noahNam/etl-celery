from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.kapt_spider import (
    KaptSpider,
)
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case import BaseSyncUseCase

logger = logger_.getLogger(__name__)


class KaptOpenApiUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=KaptSpider)
        self._spider_input_params: list[KaptOpenApiInputEntity] = list()

    def setup(self):
        self._spider_input_params: list[KaptOpenApiInputEntity] = self._repo.find_all(
            find_type=KaptFindTypeEnum.KAPT_OPEN_API_INPUT.value
        )
