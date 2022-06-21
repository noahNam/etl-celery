from uuid import uuid4

from modules.adapter.infrastructure.celery.etl_queue import etl_celery
from modules.adapter.infrastructure.sqlalchemy.context import SessionContextManager
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import SyncBldDealRepository
from modules.adapter.infrastructure.sqlalchemy.repository.govt_bld_repository import (
    SyncGovtBldRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.real_estate_repository import (
    SyncRealEstateRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import (
    SyncSubscriptionInfoRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.etl.datalake.v1.subs_info_use_case import (
    SubscriptionInfoUseCase,
)
from modules.application.use_case.etl.datamart.v1.dong_type_use_case import DongTypeUseCase
from modules.application.use_case.etl.datamart.v1.private_sale_detail_use_case import PrivateSaleDetailUseCase
from modules.application.use_case.etl.datamart.v1.private_sale_use_case import (
    PrivateSaleUseCase,
)
from modules.application.use_case.etl.datamart.v1.real_estate_use_case import (
    RealEstateUseCase,
)
from modules.application.use_case.etl.warehouse.v1.basic_use_case import BasicUseCase
from modules.application.use_case.etl.warehouse.v1.subscription_use_case import (
    SubscriptionUseCase,
)


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
    elif topic == TopicEnum.ETL_WH_SUBS_INFOS.value:
        return SubscriptionUseCase(
            topic=topic,
            subscription_repo=SyncSubscriptionRepository(session_factory=db.session),
            subs_info_repo=SyncSubscriptionInfoRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_MART_REAL_ESTATES.value:
        return RealEstateUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(session_factory=db.session),
            real_estate_repo=SyncRealEstateRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_MART_PRIVATE_SALES.value:
        return PrivateSaleUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(session_factory=db.session),
            private_sale_repo=SyncPrivateSaleRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_MART_DONG_TYPE_INFOS.value:
        return DongTypeUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(session_factory=db.session),
            private_sale_repo=SyncPrivateSaleRepository(session_factory=db.session),
        )
    elif topic == TopicEnum.ETL_MART_PRIVATE_SALE_DETAILS.value:
        return PrivateSaleDetailUseCase(
            topic=topic,
            bld_deal_repo=SyncBldDealRepository(session_factory=db.session),
            private_sale_repo=SyncPrivateSaleRepository(session_factory=db.session),
            kapt_repo=SyncKaptRepository(session_factory=db.session),
        )


@etl_celery.task
def start_worker(topic):
    session_id = str(uuid4())
    context = SessionContextManager.set_context_value(session_id)

    uc = get_task(topic=topic)
    uc.execute()

    SessionContextManager.reset_context(context=context)
