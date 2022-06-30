from typing import Callable, AsyncContextManager, Type, List, Dict

from sqlalchemy import exc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.datalake.kapt.interface.kapt_repository import KaptRepository
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldTopInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptOpenApiInputEntity,
    KakaoApiInputEntity,
    KaptBasicInfoEntity,
    KaptAreaInfoEntity,
    KaptLocationInfoEntity,
    KaptMgmtCostEntity,
    KaptMappingEntity,
)
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.code_rule_model import (
    CodeRuleModel,
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
from modules.adapter.infrastructure.sqlalchemy.repository import (
    BaseAsyncRepository,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class AsyncKaptRepository(KaptRepository, BaseAsyncRepository):
    def __init__(
        self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]
    ):
        super().__init__(session_factory=session_factory)

    async def find_by_id(
        self, house_id: int, find_type: int = 0
    ) -> KaptOpenApiInputEntity | None:
        async with self.session_factory() as session:
            kapt_basic_info = await session.get(KaptBasicInfoModel, house_id)

        if not kapt_basic_info:
            return None
        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return kapt_basic_info.to_kakao_api_input_entity()

        return kapt_basic_info.to_open_api_input_entity()

    async def find_all(self, find_type: int = 0) -> list[KaptOpenApiInputEntity]:
        async with self.session_factory() as session:
            queryset = await session.execute(select(KaptBasicInfoModel))

        if not queryset:
            return list()

        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return [query.to_kakao_api_input_entity() for query in queryset]

        return [query.to_open_api_input_entity() for query in queryset.scalars().all()]

    async def save(
        self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None
    ) -> None:
        if not kapt_orm:
            return None

        async with self.session_factory() as session:
            session.add(kapt_orm)
            await session.commit()

        return None


class SyncKaptRepository(KaptRepository):
    def find_by_id(
        self, house_id: int, find_type: int = 0
    ) -> KaptOpenApiInputEntity | KakaoApiInputEntity | None:
        kapt_basic_info = session.get(KaptBasicInfoModel, house_id)

        if not kapt_basic_info:
            return None

        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return kapt_basic_info.to_kakao_api_input_entity()

        return kapt_basic_info.to_open_api_input_entity()

    def find_all(
        self, find_type: int = 0
    ) -> list[KaptOpenApiInputEntity] | list[KakaoApiInputEntity] | list[
        KaptMappingEntity
    ]:
        queryset = session.execute(select(KaptBasicInfoModel)).scalars().all()

        if not queryset:
            return list()

        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return [query.to_kakao_api_input_entity() for query in queryset]
        elif find_type == KaptFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.value:
            return [result.to_entity_for_bld_mapping_results() for result in queryset]
        elif find_type == KaptFindTypeEnum.KAPT_BASIC_INFOS.value:
            return [query.to_kapt_basic_info_entity() for query in queryset]

        return [query.to_open_api_input_entity() for query in queryset]

    def save(self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None) -> None:
        if not kapt_orm:
            return None

        try:
            session.add(kapt_orm)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncKaptRepository][save] kapt_code : {kapt_orm.kapt_code} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

        return None

    def is_exists_by_kapt_code(
        self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None
    ) -> bool:
        result = None
        if isinstance(kapt_orm, KaptAreaInfoModel):
            query = (
                select(KaptAreaInfoModel.kapt_code)
                .filter_by(kapt_code=kapt_orm.kapt_code)
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        elif isinstance(kapt_orm, KaptLocationInfoModel):
            query = (
                select(KaptLocationInfoModel.kapt_code)
                .filter_by(kapt_code=kapt_orm.kapt_code)
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        if result:
            return True
        return False

    def update_place_id(self, house_id: int, place_id: int) -> None:
        if not house_id or not place_id:
            return None
        session.execute(
            update(KaptBasicInfoModel)
            .where(KaptBasicInfoModel.house_id == house_id)
            .values(place_id=place_id)
        )
        session.commit()
        return None

    def find_to_update(
        self,
        target_model: Type[
            KaptBasicInfoModel
            | KaptAreaInfoModel
            | KaptLocationInfoModel
            | KaptMgmtCostModel
        ],
    ) -> list[
        KaptBasicInfoEntity
        | KaptAreaInfoEntity
        | KaptLocationInfoEntity
        | KaptMgmtCostEntity
    ] | None:
        result_list = None

        if target_model == KaptBasicInfoModel:
            # 단지 기본정보
            query = select(KaptBasicInfoModel).where(
                KaptBasicInfoModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_basic_info_entity() for result in results]

        elif target_model == KaptAreaInfoModel:
            # 단지 면적정보
            query = select(KaptAreaInfoModel).where(
                KaptAreaInfoModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_area_info_entity() for result in results]

        elif target_model == KaptLocationInfoModel:
            # 단지 주변정보
            query = select(KaptLocationInfoModel).where(
                KaptLocationInfoModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_kapt_location_info_entity() for result in results
                ]

        elif target_model == KaptMgmtCostModel:
            # 단지 관리비정보
            query = select(KaptMgmtCostModel).where(
                KaptMgmtCostModel.update_needed == True
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_mgmt_cost_entity() for result in results]

        return result_list

    def find_id_by_code_rules(self, key_div: str) -> int:
        query = select(CodeRuleModel.last_seq).where(CodeRuleModel.key_div == key_div)
        return session.execute(query).scalars().first()

    def update_id_to_code_rules(self, key_div: str, last_id: int) -> None:
        session.execute(
            update(CodeRuleModel)
            .where(CodeRuleModel.key_div == key_div)
            .values(last_seq=last_id)
        )
        session.commit()

    def change_update_needed_status_by_model(
        self,
        value: [BasicInfoModel | MgmtCostModel],
    ):
        try:
            if isinstance(value, BasicInfoModel):
                session.execute(
                    update(KaptBasicInfoModel)
                    .where(KaptBasicInfoModel.kapt_code == value.kapt_code)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(value, MgmtCostModel):
                session.execute(
                    update(KaptMgmtCostModel)
                    .where(KaptMgmtCostModel.id == value.id)
                    .values(
                        update_needed=False,
                    )
                )

            session.commit()

        except exc.IntegrityError as e:
            logger.error(
                f"[SyncKaptRepository] change_update_needed_status -> {type(value)} error : {e}"
            )
            session.rollback()
            raise

    def change_update_needed_status_by_dict(
        self,
        target_model: [
            KaptLocationInfoEntity,
            KaptAreaInfoEntity,
            GovtBldTopInfoEntity,
        ],
        value: Dict,
    ):
        try:
            if isinstance(target_model, KaptLocationInfoEntity):
                session.execute(
                    update(KaptLocationInfoModel)
                    .where(KaptLocationInfoModel.kapt_code == value.get("kapt_code"))
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, KaptAreaInfoEntity):
                session.execute(
                    update(KaptAreaInfoModel)
                    .where(KaptAreaInfoModel.kapt_code == value.get("kapt_code"))
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, GovtBldTopInfoEntity):
                session.execute(
                    update(GovtBldTopInfoModel)
                    .where(GovtBldTopInfoModel.house_id == value.get("house_id"))
                    .values(
                        update_needed=False,
                    )
                )

            session.commit()

        except exc.IntegrityError as e:
            logger.error(
                f"[SyncKaptRepository] change_update_needed_status -> {type(value)} error : {e}"
            )
            session.rollback()
            raise

    def change_update_needed_status_all(
        self,
        value: List[DongInfoModel | TypeInfoModel],
    ):
        try:
            if isinstance(value, DongInfoModel):
                session.execute(
                    update(GovtBldMiddleInfoModel)
                    .where(update_needed=True)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(value, TypeInfoModel):
                session.execute(
                    update(GovtBldAreaInfoModel)
                    .where(update_needed=True)
                    .values(
                        update_needed=False,
                    )
                )

            session.commit()

        except exc.IntegrityError as e:
            logger.error(
                f"[SyncKaptRepository] change_update_needed_status -> {type(value[0])} error : {e}"
            )
            session.rollback()
            raise
