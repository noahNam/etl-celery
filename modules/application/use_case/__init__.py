import os

from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseSyncUseCase:
    def __init__(
        self,
        topic: str,
        repo,
        scrapy_settings: Settings | None = None,
    ):
        self._topic: str = topic
        self._repo = repo
        self._scrapy_settings: Settings = (
            scrapy_settings if scrapy_settings else get_project_settings()
        )
        self._crawler: Crawler | None = None
        self._spider_input_params: list = list()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"

    def execute(self):
        self.setup()

    def setup(self):
        """각 UseCase마다 직접 구현"""
        pass

    def run_crawling(self):
        process = CrawlerProcess(settings=self._scrapy_settings)
        process.crawl(
            crawler_or_spidercls=self._crawler,
            params=self._spider_input_params,
            repo=self._repo,
        )
        process.start()
        self.teardown()

    def teardown(self):
        spider_stats = self._crawler.stats.spider_stats
        logger.info(f"spider_stats: {spider_stats}")
