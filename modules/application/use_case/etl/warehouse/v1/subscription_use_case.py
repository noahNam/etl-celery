import os
from datetime import date

from modules.adapter.infrastructure.etl.dl_subs_infos import TransformSubsInfo
from modules.adapter.infrastructure.etl.wh_subscriptions import TransformSubscription
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    ApplyHomeEntity,
    GoogleSheetApplyHomeEntity,
    SubscriptionInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.applyhome_dl_model import (
    ApplyHomeModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.google_sheet_applyhome_dl_model import (
    GoogleSheetApplyHomeModel,
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

logger = logger_.getLogger(__name__)


class BaseSubscriptionUseCase:
    def __init__(
        self,
        topic: str,
        subscription_repo: SyncSubscriptionRepository,
        subs_info_repo: SyncSubscriptionInfoRepository,
    ):
        self._topic: str = topic
        self._subscription_repo: SyncSubscriptionRepository = subscription_repo
        self._subs_info_repo: SyncSubscriptionInfoRepository = subs_info_repo

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class SubscriptionUseCase(BaseSubscriptionUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        today = date.today()

        subscription_infos: list[
            SubscriptionInfoEntity
        ] | None = self._subs_info_repo.find_by_date(
            target_model=SubscriptionInfoModel, target_date=today
        )

        results: dict[
            str, list[SubscriptionModel] | list[SubscriptionDetailModel]
        ] | None = TransformSubscription().start_etl(
            from_model="subscription_infos", target_list=subscription_infos
        )

        if results:
            self.__upsert_to_warehouse(results=dict.get("subscriptions"))
            self.__upsert_to_warehouse(results=dict.get("subscription_details"))

    """
    insert, update
    """

    def __upsert_to_warehouse(
        self,
        results: list[SubscriptionModel | SubscriptionDetailModel],
    ):
        for result in results:
            exists_result: bool = self._subscription_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._subscription_repo.save(value=result)
            else:
                # update
                self._subscription_repo.update(value=result)
