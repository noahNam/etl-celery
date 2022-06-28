import re

from scrapy.crawler import Crawler

from modules.adapter.infrastructure.crawler.crawler.spiders.govt_bld_spider import (
    GovtBldSpider,
)
from modules.adapter.infrastructure.pypubsub.enum.legal_dong_code_enum import (
    LegalDongCodeTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    GovtBldInputEntity,
    KaptBasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum

from modules.application.use_case import BaseSyncUseCase
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class GovtBldUseCase(BaseSyncUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler: Crawler = Crawler(spidercls=GovtBldSpider)
        self._spider_input_params: list[GovtBldInputEntity] = list()

    def setup(self):
        self._spider_input_params: list[GovtBldInputEntity] = list()
        kapt_basic_list: list[KaptBasicInfoEntity] = self._repo.find_all(
            find_type=KaptFindTypeEnum.KAPT_BASIC_INFOS.value
        )
        legal_dong_code_infos: list[
            LegalDongCodeEntity
        ] = self.__get_all_legal_code_infos()

        if kapt_basic_list and legal_dong_code_infos:
            for basic_info in kapt_basic_list:
                patterns = list()

                if not basic_info.sido or not basic_info.sigungu:
                    continue

                if basic_info.eubmyun and not basic_info.dongri:
                    patterns.append(
                        "".join([basic_info.sido, ".*", basic_info.eubmyun, ".*"])
                    )

                if basic_info.dongri and not basic_info.eubmyun:
                    patterns.append(
                        "".join([basic_info.sido, ".*", basic_info.dongri, ".*"])
                    )

                if basic_info.sido and basic_info.sigungu:
                    patterns.append(
                        "".join([basic_info.sido, ".*", basic_info.sigungu, ".*"])
                    )

                if not patterns:
                    logger.info("not found, keep looping")
                    continue

                for pattern in patterns:
                    for dong_info in legal_dong_code_infos:
                        regex = re.compile(pattern, re.DOTALL)
                        find_result = regex.search(dong_info.locatadd_nm)

                        if find_result:
                            logger.info("Found entity, input success")
                            self._spider_input_params.append(
                                GovtBldInputEntity(
                                    house_id=basic_info.house_id,
                                    kapt_code=basic_info.kapt_code,
                                    name=basic_info.name,
                                    origin_dong_address=basic_info.origin_dong_address,
                                    new_dong_address=basic_info.new_dong_address,
                                    bjd_code=dong_info.region_cd,
                                )
                            )
                            break
        logger.info("Setup finished")

    def __get_all_legal_code_infos(self) -> list[LegalDongCodeEntity]:
        send_message(
            topic_name=LegalDongCodeTopicEnum.GET_ALL_LEGAL_CODE_INFOS.value,
        )
        return event_listener_dict.get(
            f"{LegalDongCodeTopicEnum.GET_ALL_LEGAL_CODE_INFOS.value}", list()
        )
