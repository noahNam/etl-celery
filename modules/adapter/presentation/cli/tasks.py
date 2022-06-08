from uuid import uuid4

from billiard.context import Process

from modules.adapter.infrastructure.celery.crawler_queue import celery
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.crawling.kakao_api import KakaoApiUseCase
from modules.application.use_case.crawling.kapt.v1.kapt_use_case import KaptOpenApiUseCase


def get_task(topic: str):
    if topic == TopicEnum.CRAWL_KAPT.value:
        return KaptOpenApiUseCase(
            topic=topic,
            kapt_repo=SyncKaptRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.CRAWL_KAKAO_API.value:
        return KakaoApiUseCase(
            topic=topic, kapt_repo=SyncKaptRepository(session_factory=db.session)
        )
    elif topic == TopicEnum.CRAWL_KAKAO_API.value:
        return KakaoApiUseCase(
            topic=topic, kapt_repo=SyncKaptRepository(session_factory=db.session)
        )


@celery.task
def start_crwaler(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    process = Process(target=uc.run_crawling)
    process.start()
    process.join()

    SessionContextManager.reset_context(context=context)


@celery.task
def start_worker(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    SessionContextManager.reset_context(context=context)
