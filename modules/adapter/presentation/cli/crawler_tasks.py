from billiard.context import Process

from modules.adapter.infrastructure.celery.crawler_queue import crawler_celery
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import SyncSubscriptionInfoRepository
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.crawling.govt_bld_info.v1.govt_bld_use_case import (
    GovtBldUseCase,
)
from modules.application.use_case.crawling.govt_deal.v1.govt_deal_use_case import (
    GovtDealUseCase,
)
from modules.application.use_case.crawling.kakao_api.v1.kakao_api_use_case import (
    KakaoApiUseCase,
)
from modules.application.use_case.crawling.kapt.v1.kapt_use_case import (
    KaptOpenApiUseCase,
)
from modules.application.use_case.crawling.legal_dong_code.v1.legal_code_use_case import (
    LegalCodeUseCase,
)
from modules.application.use_case.crawling.subscription_info.v1.subs_info_use_case import SubscriptionInfoUseCase


def get_task(topic: str):
    if topic == TopicEnum.CRAWL_KAPT.value:
        return KaptOpenApiUseCase(
            topic=topic,
            repo=SyncKaptRepository(),
        )
    elif topic == TopicEnum.CRAWL_KAKAO_API.value:
        return KakaoApiUseCase(topic=topic, repo=SyncKaptRepository())
    elif topic == TopicEnum.CRAWL_LEGAL_DONG_CODE.value:
        return LegalCodeUseCase(topic=topic, repo=SyncLegalDongCodeRepository())
    elif topic == TopicEnum.CRAWL_BUILDING_MANAGE.value:
        return GovtBldUseCase(topic=topic, repo=SyncKaptRepository())
    elif topic == TopicEnum.CRAWL_GOVT_DEAL_INFOS.value:
        return GovtDealUseCase(topic=topic, repo=SyncLegalDongCodeRepository())
    elif topic == TopicEnum.CRAWL_APPLY_HOME.value:
        return SubscriptionInfoUseCase(topic=topic, repo=SyncSubscriptionInfoRepository())


@crawler_celery.task
def start_crawler(topic):
    uc = get_task(topic=topic)
    uc.execute()

    process = Process(target=uc.run_crawling)
    process.start()
    process.join()

    session.remove()
