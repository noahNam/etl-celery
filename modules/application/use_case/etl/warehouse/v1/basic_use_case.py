import os
from typing import Type, Any

from modules.adapter.infrastructure.etl.wh_basic_infos import TransformBasic
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldTopInfoEntity,
    GovtBldMiddleInfoEntity,
    GovtBldAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptBasicInfoEntity,
    KaptMgmtCostEntity,
    KaptLocationInfoEntity,
    KaptAreaInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_area_info_model import (
    GovtBldAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_middle_info_model import (
    GovtBldMiddleInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_top_info_model import (
    GovtBldTopInfoModel,
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
from modules.adapter.infrastructure.sqlalchemy.repository.govt_bld_repository import (
    SyncGovtBldRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class BaseBasicUseCase:
    def __init__(
        self,
        topic: str,
        basic_repo: SyncBasicRepository,
        kapt_repo: SyncKaptRepository,
        kakao_repo: SyncKakaoApiRepository,
        govt_bld_repo: SyncGovtBldRepository,
    ):
        self._topic: str = topic
        self._basic_repo: SyncBasicRepository = basic_repo
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._kakao_repo: SyncKakaoApiRepository = kakao_repo
        self._govt_bld_repo: SyncGovtBldRepository = govt_bld_repo
        self._transfer: TransformBasic = TransformBasic()

    @property
    def client_id(self) -> str:
        return f"{self._topic}-{os.getpid()}"


class BasicUseCase(BaseBasicUseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        # 단지 기본 정보
        kapt_basic_infos: list[
            KaptBasicInfoEntity
        ] | None = self._kapt_repo.find_to_update(target_model=KaptBasicInfoModel)
        basic_infos: list[BasicInfoModel] | None = self._transfer.start_etl(
            from_model="kapt_basic_infos", target_list=kapt_basic_infos
        )

        if basic_infos:
            # 카카오 place 좌표 맵핑
            for basic_info in basic_infos:
                if not basic_info.place_id:
                    continue

                kakao_api_result: KakaoApiResultEntity | None = (
                    self._kakao_repo.find_by_id(id=basic_info.place_id)
                )
                basic_info.bld_name = kakao_api_result.bld_name
                basic_info.place_dong_address = kakao_api_result.jibun_address
                basic_info.place_road_address = kakao_api_result.road_address
                basic_info.x_vl = kakao_api_result.x_vl
                basic_info.y_vl = kakao_api_result.y_vl

            self.__upsert_to_warehouse(results=basic_infos)

        # 단지 관리비 정보
        kapt_mgmt_costs: list[
            KaptMgmtCostEntity
        ] | None = self._kapt_repo.find_to_update(target_model=KaptMgmtCostModel)
        self.__bind_house_id(target_list=kapt_mgmt_costs)

        mgmt_costs: list[MgmtCostModel] | None = self._transfer.start_etl(
            from_model="kapt_mgmt_costs", target_list=kapt_mgmt_costs
        )

        if mgmt_costs:
            self.__upsert_to_warehouse(results=mgmt_costs)

        # 단지 주변 정보
        kapt_location_infos: list[
            KaptLocationInfoEntity
        ] | None = self._kapt_repo.find_to_update(target_model=KaptLocationInfoModel)
        self.__bind_house_id(target_list=kapt_location_infos)

        location_infos: list[dict] | None = self._transfer.start_etl(
            from_model="kapt_location_infos", target_list=kapt_location_infos
        )

        if location_infos:
            self.__update_to_warehouse(
                target_model=BasicInfoModel, results=location_infos
            )

        # 단지 면적 정보
        kapt_area_infos: list[
            KaptAreaInfoEntity
        ] | None = self._kapt_repo.find_to_update(target_model=KaptAreaInfoModel)
        self.__bind_house_id(target_list=kapt_area_infos)

        area_infos: list[dict] | None = self._transfer.start_etl(
            from_model="kapt_area_infos", target_list=kapt_area_infos
        )

        if area_infos:
            self.__update_to_warehouse(target_model=BasicInfoModel, results=area_infos)

        # todo. 총괄부는 크롤링 데이터가 없는 상태라 ETL 확인 필요함. 특히, TransformBasic._etl_govt_bld_area_infos 함수
        # 총괄부 표제 단지 정보
        govt_bld_top_infos: list[
            GovtBldTopInfoEntity
        ] | None = self._govt_bld_repo.find_to_update(target_model=GovtBldTopInfoModel)
        bld_top_infos: list[dict] | None = self._transfer.start_etl(
            from_model="govt_bld_top_infos", target_list=govt_bld_top_infos
        )
        if bld_top_infos:
            self.__update_to_warehouse(
                target_model=BasicInfoModel, results=bld_top_infos
            )

        # 총괄부 표제 동 정보
        govt_bld_middle_infos: list[
            GovtBldMiddleInfoEntity
        ] | None = self._govt_bld_repo.find_to_update(
            target_model=GovtBldMiddleInfoModel
        )

        bld_middle_infos: list[DongInfoModel] | None = self._transfer.start_etl(
            from_model="govt_bld_middle_infos", target_list=govt_bld_middle_infos
        )

        if bld_middle_infos:
            self.__upsert_to_warehouse(results=bld_middle_infos)

        # 총괄부 표제 타입 정보
        govt_bld_area_infos: list[
            GovtBldAreaInfoEntity
        ] | None = self._govt_bld_repo.find_to_update(target_model=GovtBldAreaInfoModel)

        bld_area_infos: list[TypeInfoModel] | None = self._transfer.start_etl(
            from_model="govt_bld_area_infos", target_list=govt_bld_area_infos
        )

        if bld_area_infos:
            self.__upsert_to_warehouse(results=bld_area_infos)

        target_dict = dict(
            kapt_basic_infos=kapt_basic_infos,
            kapt_mgmt_costs=kapt_mgmt_costs,
            kapt_location_infos=kapt_location_infos,
            kapt_area_infos=kapt_area_infos,
            govt_bld_top_infos=govt_bld_top_infos,
            govt_bld_middle_infos=govt_bld_middle_infos,
            govt_bld_area_infos=govt_bld_area_infos,
        )

        self.__change_update_needed_status(target_dict=target_dict)

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
        results: list[BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel],
    ) -> None:
        for result in results:
            exists_result: bool = self._basic_repo.exists_by_key(value=result)

            if not exists_result:
                # insert
                self._basic_repo.save(value=result)
            else:
                # update
                self._basic_repo.update(value=result)

    """
    only update
    """

    def __update_to_warehouse(
        self,
        target_model: Type[BasicInfoModel],
        results: list[dict],
    ) -> None:
        for result in results:
            # update
            self._basic_repo.dynamic_update(target_model=target_model, value=result)

    def __change_update_needed_status(
        self,
        target_dict: dict[
            str,
            list[
                KaptBasicInfoEntity
                | KaptMgmtCostEntity
                | KaptLocationInfoEntity
                | KaptAreaInfoEntity
                | GovtBldTopInfoEntity
                | GovtBldMiddleInfoEntity
                | GovtBldAreaInfoEntity
            ],
        ],
    ):
        for key in target_dict.keys():
            target_list = target_dict.get(key)
            if target_list:
                self._kapt_repo.change_update_needed_status(target_list=target_list)
