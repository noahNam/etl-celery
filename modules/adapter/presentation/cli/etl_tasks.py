from uuid import uuid4

from modules.adapter.infrastructure.celery.etl_queue import etl_celery
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_bld_repository import (
    SyncGovtBldRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import (
    SyncSubscriptionInfoRepository,
)
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.etl.datalake.v1.subs_info_use_case import (
    SubscriptionInfoUseCase,
)
from modules.application.use_case.etl.warehouse.v1.basic_use_case import BasicUseCase


def get_task(topic: str):
    if topic == TopicEnum.ETL_WH_BASIC_INFOS.value:
        return BasicUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(session_factory=db.session),
            kapt_repo=SyncKaptRepository(session_factory=db.session),
            kakao_repo=SyncKakaoApiRepository(session_factory=db.session),
            govt_bld_repo=SyncGovtBldRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_DL_SUBS_INFOS.value:
        return SubscriptionInfoUseCase(
            topic=topic,
            subs_info_repo=SyncSubscriptionInfoRepository(session_factory=db.session),
        )


@etl_celery.task
def start_worker(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    SessionContextManager.reset_context(context=context)
