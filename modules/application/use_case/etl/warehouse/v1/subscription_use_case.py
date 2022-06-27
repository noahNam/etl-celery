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

logger = logger_.getLogger(__name__)


class SubscriptionUseCase(BaseETLUseCase):
    def __init__(
        self,
        subscription_repo: SyncSubscriptionRepository,
        subs_info_repo: SyncSubscriptionInfoRepository,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._subs_info_repo: SyncSubscriptionInfoRepository = subs_info_repo
        self._transfer: TransformSubscription = TransformSubscription()

    def execute(self):
        # DL:subscription_infos -> WH: subscriptions, subscription_details
        subscription_infos: list[
            SubscriptionInfoEntity
        ] | None = self._subs_info_repo.find_to_update(
            target_model=SubscriptionInfoModel
        )

        results: dict[
            str, list[SubscriptionModel] | list[SubscriptionDetailModel]
        ] | None = self._transfer.start_etl(
            from_model="subscription_infos", target_list=subscription_infos
        )
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
            from_model="subscription_manual_infos",
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
            self._subscription_repo.change_update_needed_status(
                target_list=update_needed_target_entities
            )
