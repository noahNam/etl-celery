# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from pydantic import BaseModel, Field


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KaptBasisInfoItem(BaseModel):
    url: str = Field()
    kapt_code: str = Field()
    kapt_name: str = Field()
    kapt_addr: str = Field()
