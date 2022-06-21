import os

from modules.adapter.infrastructure.etl.mart_private_sales import TransformPrivateSale
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BasePrivateSaleDetailUseCase:
    def __init__(
        self,
        topic: str,
        basic_repo: SyncBasicRepository,
        private_sale_repo: SyncPrivateSaleRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._private_sale_repo: SyncPrivateSaleRepository = private_sale_repo
        self._transfer: TransformPrivateSale = TransformPrivateSale()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class PrivateSaleDetailUseCase(BasePrivateSaleDetailUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        pass
        # 아파트 실거래가 정보
        # basic_infos: list[BasicInfoEntity] | None = self._basic_repo.find_to_update(
        #     target_model=BasicInfoModel
        # )

        # 아파트 전월세

        # 오피스텔 실거래가

        # 오피스텔 전월세

        # 분양권 전매

        # results: list[PrivateSaleModel] | None = self._transfer.start_etl(
        #     from_model="basic_infos", target_list=basic_infos, options=mgmt_costs
        # )
        #
        # if results:
        #     self.__upsert_to_warehouse(results=results)

    """
    insert, update
    """

    def __upsert_to_warehouse(
        self,
        results: list[PrivateSaleModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._private_sale_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._private_sale_repo.save(value=result)
            else:
                # update
                self._private_sale_repo.update(value=result)
