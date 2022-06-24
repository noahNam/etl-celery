import os

from modules.adapter.infrastructure.etl.mart_dong_type_infos import (
    TransformDongTypeInfos,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    DongInfoEntity,
    TypeInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.type_info_model import (
    TypeInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseDongTypeUseCase:
    def __init__(
        self,
        topic: str,
        basic_repo: SyncBasicRepository,
        private_sale_repo: SyncPrivateSaleRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._private_sale_repo: SyncPrivateSaleRepository = private_sale_repo
        self._transfer: TransformDongTypeInfos = TransformDongTypeInfos()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class DongTypeUseCase(BaseDongTypeUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        # 동 기본 정보
        dong_infos: list[DongInfoEntity] | None = self._basic_repo.find_to_update(
            target_model=DongInfoModel
        )
        results: list[DongInfoModel] | None = self._transfer.start_etl(
            from_model="dong_infos", target_list=dong_infos
        )

        if results:
            self.__upsert_to_datamart(results=results)

        # 타입 기본 정보
        type_infos: list[TypeInfoEntity] | None = self._basic_repo.find_to_update(
            target_model=TypeInfoModel
        )
        results: list[TypeInfoModel] | None = self._transfer.start_etl(
            from_model="type_infos", target_list=type_infos
        )

        if results:
            self.__upsert_to_datamart(results=results)

    """
    insert, update
    """

    def __upsert_to_datamart(
        self,
        results: list[DongInfoModel | TypeInfoModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._private_sale_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._private_sale_repo.save(value=result)
            else:
                # update
                self._private_sale_repo.update(value=result)

            self._basic_repo.change_update_needed_status(value=result)
