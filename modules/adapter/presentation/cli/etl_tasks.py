from uuid import uuid4

from modules.adapter.infrastructure.celery.etl_queue import etl_celery
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_apt_deals_repository import (
    SyncGovtAptDealsRepository
)

from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository
)

from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.etl.warehouse.v1.basic_use_case import BasicUseCase
from modules.application.use_case.etl.datalake.v1.mapping_use_case import BldMappingResultsUseCase


def get_task(topic: str):
    if topic == TopicEnum.ETL_WH_BASIC_INFOS.value:
        return BasicUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(session_factory=db.session),
            kapt_repo=SyncKaptRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_DL_BLD_MAPPING_RESULTS.value:
        return BldMappingResultsUseCase(
            topic=topic,
            kapt_repo=SyncKaptRepository(session_factory=db.session),
            govt_repo=SyncGovtAptDealsRepository(session_factory=db.session),
            dong_code_repo=SyncLegalDongCodeRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session)
        )

@etl_celery.task
def start_worker(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    SessionContextManager.reset_context(context=context)
