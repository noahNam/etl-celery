import os
from typing import Type

from modules.adapter.infrastructure.etl.wh_basic_infos import TransformBasic
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import KaptBasicInfoEntity, \
    KaptMgmtCostEntity
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import \
    KaptBasicInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_mgmt_cost_model import KaptMgmtCostModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import BasicInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import DongInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import MgmtCostModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.type_info_model import TypeInfoModel
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import SyncBasicRepository
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import SyncKaptRepository
from datetime import date
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseBasicUseCase:
    def __init__(
            self,
            topic: str,
            basic_repo: SyncBasicRepository,
            kapt_repo: SyncKaptRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._kapt_repo: SyncKaptRepository = kapt_repo

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class BasicUseCase(BaseBasicUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        today = date.today()
        # 단지 기본 정보
        kapt_basic_infos: list[KaptBasicInfoEntity] | None = self._kapt_repo.find_by_date(target_model=KaptBasicInfoModel, target_date=today)
        results: list[BasicInfoModel] = TransformBasic().start_etl(from_model="kapt_basic_infos", target_list=kapt_basic_infos)
        if results:
            self.__save_to_warehouse(target_model=BasicInfoModel, results=results)

        # 단지 관리비 정보
        kapt_mgmt_costs: list[KaptMgmtCostEntity] | None = self._kapt_repo.find_by_date(target_model=KaptMgmtCostModel, target_date=today)
        for kapt_mgmt_cost in kapt_mgmt_costs:
            kapt_mgmt_cost.house_id = self._basic_repo.find_house_id_by_code(kapt_code=kapt_mgmt_cost.kapt_code)

        results: list[MgmtCostModel] = TransformBasic().start_etl(from_model="kapt_mgmt_costs", target_list=kapt_mgmt_costs)

        if results:
            self.__save_to_warehouse(target_model=MgmtCostModel, results=results)

    def __save_to_warehouse(self, target_model: Type[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel], results: list[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel]):
        for result in results:
            exists_result: bool = self._basic_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._basic_repo.save(target_model=target_model, value=result)
            else:
                # update
                self._basic_repo.update(target_model=target_model, value=result)