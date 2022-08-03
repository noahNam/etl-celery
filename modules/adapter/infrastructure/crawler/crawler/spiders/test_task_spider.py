from scrapy import Spider

from modules.adapter.infrastructure.slack.slack_mixin import SlackMixin
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class TestTaskSpider(Spider, SlackMixin):
    name = "test_celery_task"

    def __init__(self, name=None, **kwargs):
        super().__init__()
        logger.info("[TestTaskSpider] init start\n")

    def parse(self, response, **kwargs):
        logger.info("[TestTaskSpider][parse] parsing\n")
