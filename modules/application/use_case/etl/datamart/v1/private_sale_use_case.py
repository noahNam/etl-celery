import json
import os
from typing import Any

from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.etl.mart_private_sales import TransformPrivateSale
from modules.adapter.infrastructure.message.broker.redis import RedisClient
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
    CalcMgmtCostEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
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
        redis: RedisClient,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._private_sale_repo: SyncPrivateSaleRepository = private_sale_repo
        self._transfer: TransformPrivateSale = TransformPrivateSale()
        self._redis: RedisClient = redis

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
            self.__upsert_to_datamart(results=results)

    """
    insert, update
    """

    def __upsert_to_datamart(
        self,
        results: list[PrivateSaleModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._private_sale_repo.exists_by_key(value=result)

            try:
                if not exists_result:
                    # insert
                    self._private_sale_repo.save(value=result)
                    key_div = "I"
                else:
                    # update
                    self._private_sale_repo.update(value=result)
                    key_div = "U"

                self._basic_repo.change_update_needed_status(value=result)

                # message publish to redis
                self._redis.set(
                    key=f"sync:{key_div}:private_sales:{result.id}",
                    value=json.dumps(result.to_dict(), ensure_ascii=False).encode(
                        "utf-8"
                    ),
                )
                self._private_sale_repo.change_update_needed_status(value=result)

            except Exception as e:
                logger.error(f"☠️\tPrivateSaleUseCase - Failure! {result.id}:{e}")
                self.__save_crawling_failure(
                    failure_value=result,
                    ref_table="private_sales",
                    param=result,
                    reason=e,
                )

    def __save_crawling_failure(
        self,
        failure_value: PrivateSaleModel,
        ref_table: str,
        param: Any | None,
        reason: Exception,
    ) -> None:
        fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
            ref_id=failure_value.id,
            ref_table=ref_table,
            param=param,
            reason=reason,
            is_solved=False,
        )

        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )
