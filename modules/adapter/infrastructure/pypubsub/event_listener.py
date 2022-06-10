from pubsub import pub

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.etl_enum import ETLEnum
from modules.adapter.infrastructure.sqlalchemy.database import db
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.call_failure_history_repository import (
    SyncFailureRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import SyncKaptRepository

event_listener_dict = {
    f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}": None,
    f"{CallFailureTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": None,
    f"{ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value}": dict(),
}


def save_crawling_failure(fail_orm) -> None:
    SyncFailureRepository(db.session).save(fail_orm=fail_orm)
    event_listener_dict.update(
        {f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}": None}
    )


def save_kakao_crawling_result(kakao_orm: KakaoApiResultModel) -> None:
    pk = SyncKakaoApiRepository(db.session).save(kakao_orm=kakao_orm)
    event_listener_dict.update(
        {f"{CallFailureTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": pk}
    )


def get_etl_target_schemas_from_kapt(date: str) -> None:
    result_dict: dict = SyncKaptRepository(db.session).find_by_date(date=date)
    event_listener_dict.update(
        {f"{ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value}": result_dict}
    )


pub.subscribe(save_crawling_failure, CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value)
pub.subscribe(
    save_kakao_crawling_result, CallFailureTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value
)
pub.subscribe(
    get_etl_target_schemas_from_kapt, ETLEnum.GET_ETL_TARGET_SCHEMAS_FROM_KAPT.value
)