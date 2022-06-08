import os

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from modules.adapter.infrastructure.crawler.crawler.spiders.kakao_api_spider import (
    KakaoApiSpider,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KakaoApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseKakaoApiUseCase:
    def __init__(
        self,
        topic: str,
        kapt_repo: SyncKaptRepository,
        scrapy_settings: Settings | None = None,
    ):
        self._topic: str = topic
        self._repo: SyncKaptRepository = kapt_repo
        self._scrapy_settings: Settings = (
            scrapy_settings if scrapy_settings else get_project_settings()
        )

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class KakaoApiUseCase(BaseKakaoApiUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=KakaoApiSpider)
        self._spider_input_params: list[KakaoApiInputEntity] = list()

    def execute(self):
        self.setup()

    def setup(self):
        self._spider_input_params: list[KakaoApiInputEntity] = self._repo.find_all(
            find_type=KaptFindTypeEnum.KAKAO_API_INPUT.value
        )

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
