import os

from modules.adapter.infrastructure.etl.mart_private_sales import TransformPrivateSale
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
    CalcMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import (
    MgmtCostModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.private_sale_repository import (
    SyncPrivateSaleRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BasePrivateSaleUseCase:
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


class PrivateSaleUseCase(BasePrivateSaleUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        """
        ** 월별 관리비 추출 계산식
        1. (공용관리비계 + 개별사용료계 + 장충금월부과금 - 잡수익월수입금액) / 단지주거전용면적(priv_area) = 관리비(m2당)
        2. 전용면적 x 관리비(m2당)

        1번은 단지 기본정보이고 2번은 타입별 정보이다.
        여름관리비는 최근 관리비데이터 기준(가장 최근 YYYYMM) 7~8월
        겨울관리비는 최근 관리비데이터 기준(가장 최근 YYYYMM) 1~2월
        평균관리비는 최근 관리비데이터 기준(가장 최근 YYYYMM) 1년치 데이터

        ** trade_status(3개월 거래), deposit_status(3개월 거래)
        위 두 필드는 private_sale_details(실거래가) ETL시 계산하여 업데이트
        """

        # 단지 기본 정보
        basic_infos: list[BasicInfoEntity] | None = self._basic_repo.find_to_update(
            target_model=BasicInfoModel
        )
        # 관리비 정보
        mgmt_costs = list()
        if basic_infos:
            for basic_info in basic_infos:
                priv_area = (
                    int(float(basic_info.priv_area)) if basic_info.priv_area else None
                )
                mgmt_cost_results: list[
                    CalcMgmtCostEntity
                ] | None = self._basic_repo.find_all(
                    target_model=MgmtCostModel,
                    id=basic_info.house_id,
                    options=priv_area,
                )
                if mgmt_cost_results:
                    mgmt_costs.append(mgmt_cost_results)

        results: list[PrivateSaleModel] | None = self._transfer.start_etl(
            from_model="basic_infos", target_list=basic_infos, options=mgmt_costs
        )

        if results:
            self.__upsert_to_warehouse(results=results)

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
