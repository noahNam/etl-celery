from datetime import date
from typing import Callable, AsyncContextManager, ContextManager, Type

from sqlalchemy import exc, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from core.domain.datalake.kapt.interface.kapt_repository import KaptRepository
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import KaptOpenApiInputEntity, \
    KakaoApiInputEntity, KaptBasicInfoEntity, KaptAreaInfoEntity, KaptLocationInfoEntity, KaptMgmtCostEntity
from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_area_info_model import (
    KaptAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_basic_info_model import (
    KaptBasicInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_location_info_model import (
    KaptLocationInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.kapt_mgmt_cost_model import KaptMgmtCostModel
from modules.adapter.infrastructure.sqlalchemy.repository import (
    BaseAsyncRepository,
    BaseSyncRepository,
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


class SyncKaptRepository(KaptRepository, BaseSyncRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def find_by_id(
        self, house_id: int, find_type: int = 0
    ) -> KaptOpenApiInputEntity | KakaoApiInputEntity | None:
        with self.session_factory() as session:
            kapt_basic_info = session.get(KaptBasicInfoModel, house_id)

        if not kapt_basic_info:
            return None

        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return kapt_basic_info.to_kakao_api_input_entity()

        return kapt_basic_info.to_open_api_input_entity()

    def find_all(
        self, find_type: int = 0
    ) -> list[KaptOpenApiInputEntity] | list[KakaoApiInputEntity]:
        with self.session_factory() as session:
            queryset = session.execute(select(KaptBasicInfoModel)).scalars().all()

        if not queryset:
            return list()

        if find_type == KaptFindTypeEnum.KAKAO_API_INPUT.value:
            return [query.to_kakao_api_input_entity() for query in queryset]

        return [query.to_open_api_input_entity() for query in queryset]

    def save(self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None) -> None:
        if not kapt_orm:
            return None

        with self.session_factory() as session:
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

    def exists_by_kapt_code(
        self, kapt_orm: KaptAreaInfoModel | KaptLocationInfoModel | None
    ) -> bool:
        with self.session_factory() as session:
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
        with self.session_factory() as session:
            session.execute(
                update(KaptBasicInfoModel)
                .where(KaptBasicInfoModel.house_id == house_id)
                .values(place_id=place_id)
            )
            session.commit()
        return None

    def find_by_date(
            self, target_model: Type[KaptBasicInfoModel | KaptAreaInfoModel | KaptLocationInfoModel | KaptMgmtCostModel], target_date: date
    ) -> list[KaptBasicInfoEntity | KaptAreaInfoEntity | KaptLocationInfoEntity | KaptMgmtCostEntity] | None:
        result_list = None

        if target_model == KaptBasicInfoModel:
            # 단지 기본정보
            with self.session_factory() as session:
                query = (
                    select(KaptBasicInfoModel)
                        .where(KaptBasicInfoModel.kapt_code == "A13980014")
                        # .where(func.date(KaptBasicInfoModel.updated_at) == target_date or func.date(KaptBasicInfoModel.updated_at) == target_date)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_basic_info_entity() for result in results]

        elif target_model == KaptAreaInfoModel:
            # 단지 면적정보
            with self.session_factory() as session:
                query = (
                    select(KaptAreaInfoModel)
                        .where(func.date(KaptAreaInfoModel.created_at) == target_date or func.date(KaptAreaInfoModel.updated_at) == target_date)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_area_info_entity() for result in results]

        elif target_model == KaptLocationInfoModel:
            # 단지 주변정보
            with self.session_factory() as session:
                query = (
                    select(KaptLocationInfoModel)
                        .where(func.date(KaptLocationInfoModel.created_at) == target_date or func.date(KaptLocationInfoModel.updated_at) == target_date)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_location_info_entity() for result in results]

        elif target_model == KaptMgmtCostModel:
            # 단지 관리비정보
            with self.session_factory() as session:
                query = (
                    select(KaptMgmtCostModel)
                        # .join(KaptBasicInfoModel.kapt_mgmt_costs)
                        .where(func.date(KaptMgmtCostModel.created_at) == target_date or func.date(KaptMgmtCostModel.updated_at) == target_date)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_mgmt_cost_entity() for result in results]

        return result_list