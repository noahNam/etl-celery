# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Spider

from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BasePipeline:
    def open_spider(self, spider: Spider):
        logger.info(f"{spider.name} pipline Opened")

    def close_spider(self, spider: Spider):
        logger.info(f"{spider.name} pipline Closed")


class KaptPipeline(BasePipeline):
    def process_item(self, item, spider: Spider):
        logger.info(f"item :  !!!!!!!!!!!!!!!!")
        print(item)
        return item
