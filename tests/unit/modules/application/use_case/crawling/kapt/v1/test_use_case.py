from scrapy.crawler import Crawler, CrawlerProcess

from modules.adapter.infrastructure.crawler.crawler.spiders.test_task_spider import TestTaskSpider
from modules.adapter.infrastructure.slack.slack_mixin import SlackMixin
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case import BaseSyncUseCase

logger = logger_.getLogger(__name__)


class TestTaskUseCase(BaseSyncUseCase, SlackMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=TestTaskSpider)

    def setup(self):
        logger.info("[TestTaskUseCase][setup] init\n")
        self.send_slack_message(f"[TestTaskUseCase]", f"celery 테스트 중입니다")
        self.send_slack_message(f"[TestTaskUseCase][setup]", f"init")

    def run_crawling(self):
        logger.info("[TestTaskUseCase][run_crawling] start\n")
        self.send_slack_message(f"[TestTaskUseCase][run_crawling]", f"start")
        process = CrawlerProcess(settings=self._scrapy_settings)
        process.crawl(
            crawler_or_spidercls=self._crawler,
            repo=self._repo,
        )
        process.start()
        self.teardown()
        logger.info("[TestTaskUseCase][run_crawling] finished\n")
        self.send_slack_message(f"[TestTaskUseCase][run_crawling]", f"finished")
