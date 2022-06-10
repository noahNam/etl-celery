from pubsub import pub

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.enum.etl_enum import ETLEnum
from modules.adapter.infrastructure.pypubsub.enum.kakao_api_enum import (
    KakaoApiTopicEnum,
)
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

event_listener_dict = {
    f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}": None,
    f"{KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": None,
    f"{KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value}": False,
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
        {f"{KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value}": pk}
    )


def is_exists_by_origin_address(kakao_orm: KakaoApiResultModel) -> None:
    result = SyncKakaoApiRepository(db.session).is_exists_by_origin_address(
        kakao_orm=kakao_orm
    )
    event_listener_dict.update(
        {f"{KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value}": result}
    )


pub.subscribe(save_crawling_failure, CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value)
pub.subscribe(
    save_kakao_crawling_result, KakaoApiTopicEnum.SAVE_KAKAO_CRAWLING_RESULT.value
)
pub.subscribe(
    is_exists_by_origin_address, KakaoApiTopicEnum.IS_EXISTS_BY_ORIGIN_ADDRESS.value
)
