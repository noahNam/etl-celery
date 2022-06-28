from modules.adapter.infrastructure.celery.etl_queue import etl_celery
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_deal_repository import (
    SyncBldDealRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_bld_repository import (
    SyncGovtBldRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.public_sale_repository import (
    SyncPublicSaleRepository,
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
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.presentation.cli.enum import TopicEnum
from modules.application.use_case.etl.datalake.v1.bld_mapping_results_use_case import (
    BldMappingResultUseCase,
)
from modules.application.use_case.etl.datalake.v1.subs_info_use_case import (
    SubscriptionInfoUseCase,
)
from modules.application.use_case.etl.datamart.v1.dong_type_use_case import (
    DongTypeUseCase,
)
from modules.application.use_case.etl.datamart.v1.private_sale_detail_use_case import (
    PrivateSaleDetailUseCase,
)
from modules.application.use_case.etl.datamart.v1.private_sale_use_case import (
    PrivateSaleUseCase,
)
from modules.application.use_case.etl.datamart.v1.public_sales_use_case import (
    PublicSaleUseCase,
)
from modules.application.use_case.etl.datamart.v1.real_estate_use_case import (
    RealEstateUseCase,
)
from modules.application.use_case.etl.warehouse.v1.apt_deal_use_case import (
    AptDealUseCase,
)
from modules.application.use_case.etl.warehouse.v1.apt_rent_use_case import (
    AptRentUseCase,
)
from modules.application.use_case.etl.warehouse.v1.basic_use_case import BasicUseCase
from modules.application.use_case.etl.warehouse.v1.ofctl_deal_use_case import (
    OfctlDealUseCase,
)
from modules.application.use_case.etl.warehouse.v1.ofctl_rent_use_case import (
    OfctlRentUseCase,
)
from modules.application.use_case.etl.warehouse.v1.right_lot_out_use_case import (
    RightLotOutUseCase,
)
from modules.application.use_case.etl.warehouse.v1.subscription_use_case import (
    SubscriptionUseCase,
)
from modules.application.use_case.etl.warehouse.v1.supply_area_use_case import (
    DealSupplyAreaUseCase,
)

logger = logger_.getLogger(__name__)


def get_task(topic: str):
    if (
        topic == TopicEnum.ETL_WH_BASIC_INFOS.value
    ):  # update_needed -> False - DL.KaptBasicInfoModel, DL.KaptMgmtCostModel, DL.KaptLocationInfoModel, DL.KaptAreaInfoModel, DL.GovtBldTopInfoModel, DL.GovtBldMiddleInfoModel, DL.GovtBldAreaInfoModel
        return BasicUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(),
            kapt_repo=SyncKaptRepository(),
            kakao_repo=SyncKakaoApiRepository(),
            govt_bld_repo=SyncGovtBldRepository(),
        )
    elif topic == TopicEnum.ETL_DL_SUBS_INFOS.value:  # update_needed -> X
        return SubscriptionInfoUseCase(
            topic=topic,
            subs_info_repo=SyncSubscriptionInfoRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_SUBS_INFOS.value
    ):  # update_needed -> False - DL.SubscriptionInfoModel, DL.SubscriptionManualInfoModel
        return SubscriptionUseCase(
            topic=topic,
            subscription_repo=SyncSubscriptionRepository(),
            subs_info_repo=SyncSubscriptionInfoRepository(),
        )
    elif topic == TopicEnum.ETL_MART_REAL_ESTATES.value:  # update_needed -> X
        return RealEstateUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(),
            real_estate_repo=SyncRealEstateRepository(),
        )
    elif (
        topic == TopicEnum.ETL_MART_PRIVATE_SALES.value
    ):  # update_needed -> False - WH.BasicInfoModel
        return PrivateSaleUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(),
            private_sale_repo=SyncPrivateSaleRepository(),
        )
    elif (
        topic == TopicEnum.ETL_MART_DONG_TYPE_INFOS.value
    ):  # update_needed -> False - WH.MartDongInfoModel, WH.MartTypeInfoModel
        return DongTypeUseCase(
            topic=topic,
            basic_repo=SyncBasicRepository(),
            private_sale_repo=SyncPrivateSaleRepository(),
        )
    elif (
        topic == TopicEnum.ETL_MART_PRIVATE_SALE_DETAILS.value
    ):  # update_needed -> False - WH.AptDealModel, WH.AptRentModel, WH.OfctlDealModel, WH.OfctlRentModel, WH.RightLotOutModel
        return PrivateSaleDetailUseCase(
            topic=topic,
            bld_deal_repo=SyncBldDealRepository(),
            private_sale_repo=SyncPrivateSaleRepository(),
            kapt_repo=SyncKaptRepository(),
        )
    elif topic == TopicEnum.ETL_DL_BLD_MAPPING_RESULTS.value:  # update_needed -> X
        return BldMappingResultUseCase(
            topic=topic,
            kapt_repo=SyncKaptRepository(),
            govt_repo=SyncGovtDealRepository(),
            dong_code_repo=SyncLegalDongCodeRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_APT_DEALS.value
    ):  # update_needed -> False - DL.GovtAptDealModel
        return AptDealUseCase(
            topic=topic,
            govt_deal_repo=SyncGovtDealRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
            bld_deal_repo=SyncBldDealRepository(),
            basic_repo=SyncBasicRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_APT_RENTS.value
    ):  # update_needed -> False - DL.GovtAptRentModel
        return AptRentUseCase(
            topic=topic,
            govt_deal_repo=SyncGovtDealRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
            bld_deal_repo=SyncBldDealRepository(),
            basic_repo=SyncBasicRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_OFCTL_DEALS
    ):  # update_needed -> False - DL.GovtOfctlDealModel
        return OfctlDealUseCase(
            govt_deal_repo=SyncGovtDealRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
            bld_deal_repo=SyncBldDealRepository(),
            basic_repo=SyncBasicRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_OFCTL_RENTS.value
    ):  # update_needed -> False - DL.GovtOfctlRentModel
        return OfctlRentUseCase(
            govt_deal_repo=SyncGovtDealRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
            bld_deal_repo=SyncBldDealRepository(),
            basic_repo=SyncBasicRepository(),
        )
    elif (
        topic == TopicEnum.ETL_WH_RIGHT_LOG_OUTS.value
    ):  # update_needed -> False - DL.GovtRightLotOutModel
        return RightLotOutUseCase(
            govt_deal_repo=SyncGovtDealRepository(),
            bld_mapping_repo=SyncBldMappingResultRepository(),
            bld_deal_repo=SyncBldDealRepository(),
            basic_repo=SyncBasicRepository(),
        )
    elif topic == TopicEnum.ETL_WH_UPDATE_SUPPLY_AREA.value:  # update_needed -> X
        return DealSupplyAreaUseCase(
            basic_repo=SyncBasicRepository(),
            bld_deal_repo=SyncBldDealRepository(),
        )

    elif topic == TopicEnum.ETL_MART_PUBLIC_SALES.value:  # update_needed -> X
        return PublicSaleUseCase(
            topic=topic,
            subscription_repo=SyncSubscriptionRepository(),
            public_repo=SyncPublicSaleRepository(),
        )


@etl_celery.task
def start_worker(topic):
    try:
        uc = get_task(topic=topic)
        uc.execute()
    except Exception as e:
        logger.error(f"{topic } error : {e}")
    finally:
        session.remove()
