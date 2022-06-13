import os
from typing import Type, Any

from modules.adapter.infrastructure.etl.wh_basic_infos import TransformBasic
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptBasicInfoEntity,
    KaptMgmtCostEntity,
    KaptLocationInfoEntity,
    KaptAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import (
    KaptBasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_mgmt_cost_model import (
    KaptMgmtCostModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.basic_info_model import (
    BasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.mgmt_cost_model import (
    MgmtCostModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.type_info_model import (
    TypeInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository.basic_repository import (
    SyncBasicRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from datetime import date
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseBasicUseCase:
    def __init__(
        self,
        topic: str,
        basic_repo: SyncBasicRepository,
        kapt_repo: SyncKaptRepository,
        kakao_repo: SyncKakaoApiRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._kakao_repo: SyncKakaoApiRepository = kakao_repo

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class BasicUseCase(BaseBasicUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        today = date.today()

        # 단지 기본 정보
        kapt_basic_infos: list[
            KaptBasicInfoEntity
        ] | None = self._kapt_repo.find_by_date(
            target_model=KaptBasicInfoModel, target_date=today
        )
        results: list[BasicInfoModel] | None = TransformBasic().start_etl(
            from_model="kapt_basic_infos", target_list=kapt_basic_infos
        )

        # 카카오 place 좌표 맵핑
        for result in results:
            if not result.place_id:
                continue

            kakao_api_result: KakaoApiResultEntity | None = self._kakao_repo.find_by_id(
                id=result.place_id
            )
            result.x_vl = kakao_api_result.x_vl
            result.y_vl = kakao_api_result.y_vl

        if results:
            self.__upsert_to_warehouse(target_model=BasicInfoModel, results=results)

        # todo. road_name, road_number, land_number 추출 필요

        # # 단지 관리비 정보
        # kapt_mgmt_costs: list[KaptMgmtCostEntity] | None = self._kapt_repo.find_by_date(
        #     target_model=KaptMgmtCostModel, target_date=today
        # )
        # self.__bind_house_id(target_list=kapt_mgmt_costs)
        #
        # results: list[MgmtCostModel] | None = TransformBasic().start_etl(
        #     from_model="kapt_mgmt_costs", target_list=kapt_mgmt_costs
        # )
        #
        # if results:
        #     self.__upsert_to_warehouse(target_model=MgmtCostModel, results=results)

        # # 단지 주변 정보
        # kapt_location_infos: list[KaptLocationInfoEntity] | None = self._kapt_repo.find_by_date(
        #     target_model=KaptLocationInfoModel, target_date=today
        # )
        # self.__bind_house_id(target_list=kapt_location_infos)
        #
        # results: list[dict] | None = TransformBasic().start_etl(
        #     from_model="kapt_location_infos", target_list=kapt_location_infos
        # )
        #
        # if results:
        #     self.__update_to_warehouse(target_model=BasicInfoModel, results=results)

        # # 단지 면적 정보
        # kapt_area_infos: list[KaptAreaInfoEntity] | None = self._kapt_repo.find_by_date(
        #     target_model=KaptAreaInfoModel, target_date=today
        # )
        # self.__bind_house_id(target_list=kapt_area_infos)
        #
        # results: list[dict] | None = TransformBasic().start_etl(
        #     from_model="kapt_area_infos", target_list=kapt_area_infos
        # )
        #
        # if results:
        #     self.__update_to_warehouse(target_model=BasicInfoModel, results=results)

        # 카카오 place 좌표 맵핑
        # kapt_area_infos: list[KaptAreaInfoEntity] | None = self._kapt_repo.find_by_date(
        #     target_model=KaptAreaInfoModel, target_date=today
        # )
        # self.__bind_house_id(target_list=kapt_area_infos)
        #
        # results: list[dict] | None = TransformBasic().start_etl(
        #     from_model="kapt_area_infos", target_list=kapt_area_infos
        # )
        #
        # if results:
        #     self.__update_to_warehouse(target_model=BasicInfoModel, results=results)

    """
    key mapping
    """

    def __bind_house_id(self, target_list: list[Any]) -> None:
        if target_list:
            for target_obj in target_list:
                target_obj.house_id = self._basic_repo.find_house_id_by_code(
                    kapt_code=target_obj.kapt_code
                )

    """
    insert, update
    """

    def __upsert_to_warehouse(
        self,
        target_model: Type[
            BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
        ],
        results: list[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel],
    ):
        for result in results:
            exists_result: bool = self._basic_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._basic_repo.save(target_model=target_model, value=result)
            else:
                # update
                self._basic_repo.update(target_model=target_model, value=result)

    """
    only update
    """

    def __update_to_warehouse(
        self,
        target_model: Type[BasicInfoModel],
        results: list[dict],
    ):
        for result in results:
            # update
            self._basic_repo.dynamic_update(target_model=target_model, value=result)
