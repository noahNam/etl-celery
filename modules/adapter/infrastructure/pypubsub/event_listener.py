from pubsub import pub

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.etl_enum import ETLEnum
from modules.adapter.infrastructure.pypubsub.enum.kakao_api_enum import (
    KakaoApiTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.legal_dong_code_enum import (
    LegalDongCodeTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.subs_info_enum import (
    SubsInfoTopicEnum,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.call_failure_history_repository import (
    SyncFailureRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import (
    SyncSubscriptionInfoRepository,
)

event_listener_dict = {
    f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}": None,
    f"{KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": None,
    f"{KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value}": False,
    f"{ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value}": dict(),
    f"{CallFailureTopicEnum.IS_EXISTS.value}": False,
    f"{LegalDongCodeTopicEnum.GET_ALL_LEGAL_CODE_INFOS.value}": list(),
    f"{SubsInfoTopicEnum.BULK_SAVE_SUBSCRIPTION_INFOS.value}": None,
    f"{SubsInfoTopicEnum.SAVE_ALL.value}": None,
    f"{SubsInfoTopicEnum.UPDATE_TO_NEW_SCHEMA.value}": None,
    f"{SubsInfoTopicEnum.FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH.value}": list(),
}


def save_crawling_failure(fail_orm) -> None:
    SyncFailureRepository().save(fail_orm=fail_orm)
    event_listener_dict.update(
        {f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}": None}
    )


def save_kakao_crawling_result(kakao_orm: KakaoApiResultModel) -> None:
    pk = SyncKakaoApiRepository().save(kakao_orm=kakao_orm)
    event_listener_dict.update(
        {f"{KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": pk}
    )


def is_exists_by_origin_address(kakao_orm: KakaoApiResultModel) -> None:
    result: bool = SyncKakaoApiRepository().is_exists_by_origin_address(
        kakao_orm=kakao_orm
    )
    event_listener_dict.update(
        {f"{KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value}": result}
    )


def is_exists_failure(fail_orm: CallFailureHistoryModel) -> None:
    result: bool = SyncFailureRepository().is_exists(fail_orm=fail_orm)
    event_listener_dict.update({f"{CallFailureTopicEnum.IS_EXISTS.value}": result})


def get_all_legal_code_infos() -> None:
    result: list[LegalDongCodeEntity] = SyncLegalDongCodeRepository().find_all()
    event_listener_dict.update(
        {f"{LegalDongCodeTopicEnum.GET_ALL_LEGAL_CODE_INFOS.value}": result}
    )


def bulk_save_subscription_infos(create_list: list[dict]) -> None:
    SyncSubscriptionInfoRepository().bulk_save_subscription_infos(
        create_list=create_list
    )
    event_listener_dict.update(
        {f"{SubsInfoTopicEnum.BULK_SAVE_SUBSCRIPTION_INFOS.value}": create_list}
    )


def save_all(
    values: list[SubscriptionInfoModel] | list[SubscriptionManualInfoModel],
) -> None:
    SyncSubscriptionInfoRepository().save_all(values=values)
    event_listener_dict.update({f"{SubsInfoTopicEnum.SAVE_ALL.value}": None})


def update_subs_info(subs_info: SubscriptionInfoModel) -> None:
    SyncSubscriptionInfoRepository().update_to_new_schema(value=subs_info)
    event_listener_dict.update(
        {f"{SubsInfoTopicEnum.UPDATE_TO_NEW_SCHEMA.value}": None}
    )


def find_subscription_infos_by_year_month(
    start_year_month: str, end_year_month: str
) -> None:
    result: list[
        SubscriptionInfoEntity
    ] = SyncSubscriptionInfoRepository().find_subscription_infos_by_year_month(
        start_year_month=start_year_month, end_year_month=end_year_month
    )
    event_listener_dict.update(
        {f"{SubsInfoTopicEnum.FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH.value}": result}
    )


pub.subscribe(save_crawling_failure, CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value)
pub.subscribe(
    save_kakao_crawling_result, KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value
)
pub.subscribe(
    is_exists_by_origin_address, KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value
)
pub.subscribe(is_exists_failure, CallFailureTopicEnum.IS_EXISTS.value)
pub.subscribe(
    get_all_legal_code_infos, LegalDongCodeTopicEnum.GET_ALL_LEGAL_CODE_INFOS.value
)
pub.subscribe(
    bulk_save_subscription_infos, SubsInfoTopicEnum.BULK_SAVE_SUBSCRIPTION_INFOS.value
)
pub.subscribe(save_all, SubsInfoTopicEnum.SAVE_ALL.value)
pub.subscribe(update_subs_info, SubsInfoTopicEnum.UPDATE_TO_NEW_SCHEMA.value)
pub.subscribe(
    find_subscription_infos_by_year_month,
    SubsInfoTopicEnum.FIND_SUBSCRIPTION_INFOS_BY_YEAR_MONTH.value,
)
