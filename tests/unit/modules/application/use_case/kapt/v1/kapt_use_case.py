import os
from typing import Type

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from core.domain.kapt.interface.kapt_repository import KaptRepository
from modules.adapter.infrastructure.cache.interface import Cache
from modules.adapter.infrastructure.cache.redis import RedisClient
from modules.adapter.infrastructure.crawler.crawler.spiders.kapt_spider import KaptSpider
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseKaptUseCase:
    def __init__(
            self,
            topic: str,
            kapt_repo: Type[KaptRepository],
            cache: RedisClient,
            scrapy_settings: Settings | None = None):
        self._topic: str = topic
        self._repo: Type[KaptRepository] = kapt_repo
        self._redis: Cache = cache
        self._crawler: Crawler = Crawler(spidercls=KaptSpider)
        self._scrapy_settings: Settings = scrapy_settings if scrapy_settings else get_project_settings()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class KaptOpenApiUseCase(BaseKaptUseCase):
    async def execute(self):
        # result = self._repo.find_by_id()
        print("executed!!!!!!!!!")

    def run_crawling(self):
        process = CrawlerProcess(settings=self._scrapy_settings)
        process.crawl(crawler_or_spidercls=self._crawler)
        process.start()
        self.teardown()

    def teardown(self):
        spider_stats = self._crawler.stats.spider_stats
        logger.info(f"spider_stats: {spider_stats}")

