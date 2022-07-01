from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.subscription_spider import SubscriptionSpider
from modules.application.use_case import BaseSyncUseCase
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SubscriptionInfoUseCase(BaseSyncUseCase):
    """Not used setup method in this case"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=SubscriptionSpider)

