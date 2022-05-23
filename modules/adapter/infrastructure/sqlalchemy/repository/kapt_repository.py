from typing import Callable, AsyncContextManager, ContextManager

from sqlalchemy import exc, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from core.domain.kapt.interface.kapt_repository import KaptRepository
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.entity.v1.kapt_entity import (
    KaptOpenApiInputEntity,
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

    async def find_by_id(self, house_id: int) -> KaptOpenApiInputEntity | None:
        async with self.session_factory() as session:
            kapt_basic_info = await session.get(KaptBasicInfoModel, house_id)

        if not kapt_basic_info:
            return None

        return kapt_basic_info.to_open_api_input_entity()

    async def find_all(self) -> list[KaptOpenApiInputEntity]:
        async with self.session_factory() as session:
            queryset = await session.execute(select(KaptBasicInfoModel))

        if not queryset:
            return list()

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

    def find_by_id(self, house_id: int) -> KaptOpenApiInputEntity | None:
        with self.session_factory() as session:
            kapt_basic_info = session.get(KaptBasicInfoModel, house_id)

        if not kapt_basic_info:
            return None

        return kapt_basic_info.to_open_api_input_entity()

    def find_all(self) -> list[KaptOpenApiInputEntity]:
        with self.session_factory() as session:
            queryset = session.execute(select(KaptBasicInfoModel))

        if not queryset:
            return list()

        return [query.to_open_api_input_entity() for query in queryset.scalars().all()]

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
