import os
from uuid import uuid4

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from modules.adapter.infrastructure.cache.interface import Cache
from modules.adapter.infrastructure.cache.redis import RedisClient
from modules.adapter.infrastructure.crawler.crawler.spiders.kapt_spider import (
    KaptSpider,
)
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    AsyncKaptRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseKaptUseCase:
    def __init__(
        self,
        topic: str,
        kapt_repo: AsyncKaptRepository,
        cache: RedisClient,
        scrapy_settings: Settings | None = None,
    ):
        self._topic: str = topic
        self._repo: AsyncKaptRepository = kapt_repo
        self._redis: Cache = cache
        self._scrapy_settings: Settings = (
            scrapy_settings if scrapy_settings else get_project_settings()
        )

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class KaptOpenApiUseCase(BaseKaptUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=KaptSpider)
        self._spider_input_params: list[KaptOpenApiInputEntity] = list()

    async def execute(self):
        session_id = str(uuid4())
        context = SessionContextManager.set_context_value(session_id)

        self._spider_input_params: list[
            KaptOpenApiInputEntity
        ] = await self._repo.find_all()

        SessionContextManager.reset_context(context=context)

    def run_crawling(self):
        process = CrawlerProcess(settings=self._scrapy_settings)
        process.crawl(
            crawler_or_spidercls=self._crawler, params=self._spider_input_params
        )
        process.start()
        self.teardown()

    def teardown(self):
        spider_stats = self._crawler.stats.spider_stats
        logger.info(f"spider_stats: {spider_stats}")
