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
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealsRepository
)

from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository
)
from modules.adapter.infrastructure.sqlalchemy.repository.building_deal_repository import (
    SyncBuildingDealRepository
)


from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.etl.warehouse.v1.basic_use_case import BasicUseCase
from modules.application.use_case.etl.warehouse.v1.apt_deal_use_case import AptDealUseCase
from modules.application.use_case.etl.datalake.v1.bld_mapping_results_use_case import BldMappingResultsUseCase
from modules.application.use_case.etl.warehouse.v1.apt_rent_use_case import AptRentUseCase
from modules.application.use_case.etl.warehouse.v1.ofctl_deal_use_case import OfctlDealUseCase
from modules.application.use_case.etl.warehouse.v1.ofctl_rent_use_case import OfctlRentsUseCase
from modules.application.use_case.etl.warehouse.v1.right_lot_out_use_case import RightLotOutUseCase


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
            govt_repo=SyncGovtDealsRepository(session_factory=db.session),
            dong_code_repo=SyncLegalDongCodeRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_WH_APT_DEALS.value:
        return AptDealUseCase(
            topic=topic,
            govt_deal_repo=SyncGovtDealsRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
            bld_deal_repo=SyncBuildingDealRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_WH_APT_RENTS.value:
        return AptRentUseCase(
            topic=topic,
            govt_deal_repo=SyncGovtDealsRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
            bld_deal_repo=SyncBuildingDealRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_WH_OFCTL_DEALS:
        return OfctlDealUseCase(
            govt_deal_repo=SyncGovtDealsRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
            bld_deal_repo=SyncBuildingDealRepository(session_factory=db.session)
        )
    elif topic == TopicEnum.ETL_WH_OFCTL_RENTS.value:
        return OfctlRentsUseCase(
            govt_deal_repo=SyncGovtDealsRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
            bld_deal_repo=SyncBuildingDealRepository(session_factory=db.session)
        )
    elif topic == TopicEnum.ETL_WH_RIGHT_LOG_OUTS.value:
        return RightLotOutUseCase(
            govt_deal_repo=SyncGovtDealsRepository(session_factory=db.session),
            bld_mapping_repo=SyncBldMappingResultsRepository(session_factory=db.session),
            bld_deal_repo=SyncBuildingDealRepository(session_factory=db.session)
        )
    elif topic == TopicEnum.ETL_WH_UPDATE_SUPPLY_AREA.value:
        return


@etl_celery.task
def start_worker(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    SessionContextManager.reset_context(context=context)
