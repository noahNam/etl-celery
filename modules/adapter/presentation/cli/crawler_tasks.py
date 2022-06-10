from uuid import uuid4

from billiard.context import Process

from modules.adapter.infrastructure.celery.crawler_queue import crawler_celery
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.crawling.kakao_api.v1.kakao_api_use_case import (
    KakaoApiUseCase,
)
from modules.application.use_case.crawling.kapt.v1.kapt_use_case import (
    KaptOpenApiUseCase,
)
from modules.application.use_case.legal_dong_code.v1.legal_code_use_case import (
    LegalCodeUseCase,
)


def get_task(topic: str):
    if topic == TopicEnum.CRAWL_KAPT.value:
        return KaptOpenApiUseCase(
            topic=topic,
            repo=SyncKaptRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.CRAWL_KAKAO_API.value:
        return KakaoApiUseCase(
            topic=topic, repo=SyncKaptRepository(session_factory=db.session)
        )
    elif topic == TopicEnum.CRAWL_LEGAL_DONG_CODE.value:
        return LegalCodeUseCase(
            topic=topic, repo=SyncLegalDongCodeRepository(session_factory=db.session)
        )


@crawler_celery.task
def start_crwaler(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    process = Process(target=uc.run_crawling)
    process.start()
    process.join()

    SessionContextManager.reset_context(context=context)
