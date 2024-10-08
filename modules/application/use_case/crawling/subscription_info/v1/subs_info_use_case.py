from scrapy.crawler import Crawler, CrawlerProcess

from modules.adapter.infrastructure.crawler.crawler.spiders.subs_info_spider import (
    SubscriptionSpider,
)
from modules.application.use_case import BaseSyncUseCase
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SubscriptionInfoUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=SubscriptionSpider)
        self._subs_info_last_id_seq: int = 0

    def setup(self):
        self._subs_info_last_id_seq = self._repo.find_id_by_code_rules(
            key_div="subs_id"
        )

    def run_crawling(self):
        process = CrawlerProcess(settings=self._scrapy_settings)
        process.crawl(
            crawler_or_spidercls=self._crawler,
            subs_info_last_id_seq=self._subs_info_last_id_seq,
            repo=self._repo,
        )
        process.start()
        self.teardown()
