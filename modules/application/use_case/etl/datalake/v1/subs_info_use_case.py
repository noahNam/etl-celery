from modules.adapter.infrastructure.etl.dl_subs_infos import TransformSubsInfo
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    ApplyHomeEntity,
    GoogleSheetApplyHomeEntity,
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
from modules.adapter.infrastructure.sqlalchemy.repository.subs_infos_repository import (
    SyncSubscriptionInfoRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase

logger = logger_.getLogger(__name__)


class SubscriptionInfoUseCase(BaseETLUseCase):
    def __init__(
            self,
            subs_info_repo: SyncSubscriptionInfoRepository,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subs_info_repo: SyncSubscriptionInfoRepository = subs_info_repo
        self._transfer: TransformSubsInfo = TransformSubsInfo()

    def execute(self):
        # ApplyHomeModel -> SubscriptionInfoModel
        apply_homes: list[ApplyHomeEntity] | None = self._subs_info_repo.find_all(
            target_model=ApplyHomeModel
        )

        results: list[SubscriptionInfoModel] | None = self._transfer.start_etl(
            from_model="apply_homes", target_list=apply_homes
        )
        if results:
            self.__upsert_to_datalake(results=results)

        # GoogleSheetApplyHomeModel -> SubscriptionManualInfoModel
        google_sheet_applys: list[
            GoogleSheetApplyHomeEntity
        ] | None = self._subs_info_repo.find_all(target_model=GoogleSheetApplyHomeModel)

        results: list[SubscriptionManualInfoModel] | None = self._transfer.start_etl(
            from_model="google_sheet_applys", target_list=google_sheet_applys
        )
        if results:
            self.__upsert_to_datalake(results=results)

    """
    insert, update
    """

    def __upsert_to_datalake(
        self,
        results: list[SubscriptionInfoModel | SubscriptionManualInfoModel],
    ):
        for result in results:
            exists_result: bool = self._subs_info_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._subs_info_repo.save_to_new_schema(value=result)
            else:
                # update
                self._subs_info_repo.update_to_new_schema(value=result)
