from typing import Type

from modules.adapter.infrastructure.etl.wh_subscriptions import TransformSubscription
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionInfoEntity,
    SubscriptionManualInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_manual_info_model import (
    SubscriptionManualInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_detail_model import (
    SubscriptionDetailModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import (
    SyncSubscriptionInfoRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.subscription_repository import (
    SyncSubscriptionRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kakao_api_result_model import (
    KakaoApiResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)


logger = logger_.getLogger(__name__)


class SubscriptionUseCase(BaseETLUseCase):
    def __init__(
        self,
        subscription_repo: SyncSubscriptionRepository,
        subs_info_repo: SyncSubscriptionInfoRepository,
        kakao_repo: SyncKakaoApiRepository,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._subs_info_repo: SyncSubscriptionInfoRepository = subs_info_repo
        self._kakao_repo: SyncKakaoApiRepository = kakao_repo
        self._transfer: TransformSubscription = TransformSubscription()

    def execute(self):
        # DL:subscription_infos -> WH: subscriptions, subscription_details
        subscription_infos: list[
            SubscriptionInfoEntity
        ] | None = self._subs_info_repo.find_to_update(
            target_model=SubscriptionInfoModel
        )

        # 카카오 주소 데이터 불러오기
        if subscription_infos:
            address_data: dict[
                str, list[int] | list[KakaoApiResultModel | None]
            ] = self._transfer.get_kakao_address(
                subs_infos=subscription_infos
            )
            subs_ids: list[int] = address_data.get("subs_ids")
            kakao_addresses: list[KakaoApiResultModel | None] = address_data.get("kakao_addresses")

            # kakao_api_results insert
            self.__insert_to_datalake(
                results=kakao_addresses
            )

            place_ids = list()
            for kakao_address in kakao_addresses:
                place_id: int | None = self._kakao_repo.find_to_place_id(kakao_orm=kakao_address)
                place_ids.append(place_id)

            self.__update_to_datalake(
                filter=subs_ids, values=place_ids
            )

            for subscription_info in subscription_infos:
                if subscription_info.subs_id in subs_ids:
                    idx = subs_ids.index(subscription_info.subs_id)
                    place_id = place_ids[idx]
                    subscription_info.place_id = place_id

        results: dict[
            str, list[SubscriptionModel] | list[SubscriptionDetailModel]
        ] | None = self._transfer.start_etl(target_list=subscription_infos)
        if results:
            self.__upsert_to_warehouse(results=results.get("subscriptions"))
            self.__upsert_to_warehouse(results=results.get("subscription_details"))
            self.__change_update_needed_status(
                update_needed_target_entities=subscription_infos
            )

        # DL:subscription_manual_infos -> WH: subscriptions, subscription_details
        # Only update
        subscription_manual_infos: list[
            SubscriptionManualInfoEntity
        ] | None = self._subs_info_repo.find_to_update(
            target_model=SubscriptionManualInfoModel
        )

        results: dict[str, [dict]] | None = self._transfer.start_etl(
            target_list=subscription_manual_infos,
        )
        if results:
            self.__update_to_warehouse(
                target_model=SubscriptionModel, results=results.get("subscriptions")
            )
            self.__update_to_warehouse(
                target_model=SubscriptionDetailModel,
                results=results.get("subscription_details"),
            )
            self.__change_update_needed_status(
                update_needed_target_entities=subscription_manual_infos
            )

    """
    insert, update
    """

    def __upsert_to_warehouse(
        self, results: list[SubscriptionModel | SubscriptionDetailModel]
    ):
        for result in results:
            exists_result: bool = self._subscription_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._subscription_repo.save(value=result)
            else:
                # update
                self._subscription_repo.update(value=result)

    """
    only update
    """

    def __update_to_warehouse(
        self,
        target_model: Type[SubscriptionModel | SubscriptionDetailModel],
        results: list[dict],
    ) -> None:
        for result in results:
            # update
            self._subscription_repo.dynamic_update(
                target_model=target_model, value=result
            )

    """
    all change update_needed -> False
    """

    def __change_update_needed_status(
        self,
        update_needed_target_entities: list[
            SubscriptionInfoEntity | SubscriptionManualInfoEntity
        ],
    ) -> None:
        if update_needed_target_entities:
            try:
                self._subscription_repo.change_update_needed_status(
                    target_list=update_needed_target_entities
                )

            except Exception as e:
                logger.error(
                    f"☠️\tSubscriptionUseCase - Failure! {update_needed_target_entities[0].id}:{e}"
                )
                self._save_crawling_failure(
                    failure_value=update_needed_target_entities[0].id,
                    ref_table="subscriptions"
                    if isinstance(
                        update_needed_target_entities[0], SubscriptionInfoEntity
                    )
                    else "subscription_details",
                    param=update_needed_target_entities[0],
                    reason=e,
                )

    def __insert_to_datalake(
            self,
            results: list[KakaoApiResultModel | None]
    ):
        for result in results:
            if result:
                exists_result: bool = self._kakao_repo.is_exists_by_origin_address(kakao_orm=result)
                if not exists_result:
                    # insert
                    self._kakao_repo.save(kakao_orm=result)
                else:
                    pass
            else:
                pass

    def __update_to_datalake(
            self,
            filter: list[int],
            values: list[int],
    ):
        for i in range(len(filter)):
            self._subs_info_repo.update_by_key_value(key=filter[i], value=values[i])
