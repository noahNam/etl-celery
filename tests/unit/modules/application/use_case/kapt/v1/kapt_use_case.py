import os
from typing import Type

from scrapy.crawler import Crawler

from core.domain.kapt.interface.kapt_repository import KaptRepository
from modules.adapter.infrastructure.cache.interface import Cache
from modules.adapter.infrastructure.cache.redis import RedisClient
from modules.adapter.infrastructure.crawler.crawler.spiders.kapt_spider import KaptSpider
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseKaptUseCase:
    def __init__(self, topic: str, kapt_repo: Type[KaptRepository], cache: RedisClient):
        self._topic: str = topic
        self._repo: Type[KaptRepository] = kapt_repo
        self._redis: Cache = cache
        self._crawler: Crawler = Crawler(spidercls=KaptSpider)

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class KaptOpenApiUseCase(BaseKaptUseCase):
    async def execute(self):
        print("executed")
        print(self.client_id)
