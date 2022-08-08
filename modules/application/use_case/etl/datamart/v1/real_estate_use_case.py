import json

from modules.adapter.infrastructure.etl.mart_real_estates import TransformRealEstate
from modules.adapter.infrastructure.message.broker.redis import RedisClient
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.real_estate_repository import (
    SyncRealEstateRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase

logger = logger_.getLogger(__name__)


class RealEstateUseCase(BaseETLUseCase):
    def __init__(
        self,
        basic_repo: SyncBasicRepository,
        real_estate_repo: SyncRealEstateRepository,
        subs_repo: SyncSubscriptionRepository,
        dong_code_repo: SyncLegalDongCodeRepository,
        kakao_api: SyncKakaoApiRepository,
        redis: RedisClient,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._basic_repo: SyncBasicRepository = basic_repo
        self._real_estate_repo: SyncRealEstateRepository = real_estate_repo
        self._subs_repo: SyncSubscriptionRepository = subs_repo
        self._transfer: TransformRealEstate = TransformRealEstate()
        self._dong_code: SyncLegalDongCodeRepository = dong_code_repo
        self._kakao_api: SyncKakaoApiRepository = kakao_api
        self._redis: RedisClient = redis


    def execute(self):
        """
        1. real_estates.id ==  place_id
        2. place_id가 없는 경우 mart로 etl 하지 않음 (의미가 없기 때문에)
        """
        # 단지 기본 정보
        basic_infos: list[BasicInfoEntity] | None = self._basic_repo.find_to_update(
            target_model=BasicInfoModel
        )

        subscriptions: list[SubscriptionModel] | None = self._subs_repo.find_by_update_needed(
            model=SubscriptionModel
        )
        if subscriptions:
            place_ids: list[int | None] = self._transfer.get_place_id(subscriptions=subscriptions)
            kakao_api_results = list()
            for place_id in place_ids:
                kakao_api_result: KakaoApiResultEntity | None = self._kakao_api.find_by_id(id=place_id)
                kakao_api_results.append(kakao_api_result)
        else:
            kakao_api_results = list()

        legal_dong_codes: list[LegalDongCodeEntity] = self._dong_code.find_all()

        results: list[RealEstateModel] | None = self._transfer.start_etl(
            basic_infos=basic_infos,
            kakao_api_results=kakao_api_results,
            legal_dong_codes=legal_dong_codes,
        )

        if results:
            self.__upsert_to_datamart(results=results)

    """
    insert, update
    """

    def __upsert_to_datamart(
        self,
        results: list[RealEstateModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._real_estate_repo.exists_by_key(value=result)

            try:
                if not exists_result:
                    # insert
                    self._real_estate_repo.save(value=result)
                else:
                    # update
                    self._real_estate_repo.update(value=result)

                # message publish to redis
                self._redis.set(
                    key=f"sync:real_estates:{result.id}",
                    value=json.dumps(result.to_dict(), ensure_ascii=False).encode(
                        "utf-8"
                    ),
                )
                self._real_estate_repo.change_update_needed_status(value=result)

            except Exception as e:
                logger.error(f"☠️\tRealEstateUseCase - Failure! {result.id}:{e}")
                self._save_crawling_failure(
                    failure_value=result.id,
                    ref_table="real_estates",
                    param=result,
                    reason=e,
                )
