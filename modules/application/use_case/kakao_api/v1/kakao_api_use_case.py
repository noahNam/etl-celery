from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.kakao_api_spider import (
    KakaoApiSpider,
)
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KakaoApiInputEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum
from modules.application.use_case import BaseSyncUseCase


class KakaoApiUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=KakaoApiSpider)
        self._spider_input_params: list[KakaoApiInputEntity] = list()

    def setup(self):
        self._spider_input_params: list[KakaoApiInputEntity] = self._repo.find_all(
            find_type=KaptFindTypeEnum.KAKAO_API_INPUT.value
        )
