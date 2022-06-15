from datetime import date
from typing import Type

from sqlalchemy import select, exc, func

from core.domain.datalake.govt_bld_info.interface.govt_bld_info_repository import (
    GovtBldRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_bld_entity import (
    GovtBldTopInfoEntity,
    GovtBldMiddleInfoEntity,
    GovtBldAreaInfoEntity,
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
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncGovtBldRepository(BaseSyncRepository, GovtBldRepository):
    def save(
        self,
        bld_orm: GovtBldTopInfoModel
        | GovtBldMiddleInfoModel
        | GovtBldAreaInfoModel
        | None,
    ) -> None:
        if not bld_orm:
            return None

        with self.session_factory() as session:
            try:
                session.add(bld_orm)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncKaptRepository][save] mgm_bldrgst_pk : {bld_orm.mgm_bldrgst_pk} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException

        return None

    def is_exists(
        self, bld_orm: GovtBldTopInfoModel | GovtBldMiddleInfoModel | None
    ) -> bool:
        with self.session_factory() as session:
            if isinstance(bld_orm, GovtBldTopInfoModel):
                query = (
                    select(GovtBldTopInfoModel)
                    .filter_by(mgm_bldrgst_pk=bld_orm.mgm_bldrgst_pk)
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

            elif isinstance(bld_orm, GovtBldMiddleInfoModel):
                query = (
                    select(GovtBldMiddleInfoModel)
                    .filter_by(mgm_bldrgst_pk=bld_orm.mgm_bldrgst_pk)
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

            elif isinstance(bld_orm, GovtBldAreaInfoModel):
                query = (
                    select(GovtBldAreaInfoModel)
                    .filter_by(mgm_bldrgst_pk=bld_orm.mgm_bldrgst_pk)
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

        if result:
            return True
        return False

    def find_by_date(
        self,
        target_model: Type[
            GovtBldTopInfoModel | GovtBldMiddleInfoModel | GovtBldAreaInfoModel
        ],
        target_date: date,
    ) -> list[
        GovtBldTopInfoEntity | GovtBldMiddleInfoEntity | GovtBldAreaInfoEntity
    ] | None:
        result_list = None

        if target_model == GovtBldTopInfoModel:
            #  총괄부 표제 단지 정보
            with self.session_factory() as session:
                query = (
                    select(GovtBldTopInfoModel)
                    .where(
                        func.date(GovtBldTopInfoModel.updated_at) == target_date
                        or func.date(GovtBldTopInfoModel.updated_at) == target_date
                    )
                    .order_by(GovtBldTopInfoModel.id)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [result.to_kapt_basic_info_entity() for result in results]

        elif target_model == GovtBldMiddleInfoModel:
            # 총괄부 표제 동 정보
            with self.session_factory() as session:
                query = (
                    select(GovtBldMiddleInfoModel)
                    .where(
                        func.date(GovtBldMiddleInfoModel.created_at) == target_date
                        or func.date(GovtBldMiddleInfoModel.updated_at) == target_date
                    )
                    .order_by(GovtBldMiddleInfoModel.id)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_govt_bld_top_info_entity() for result in results
                ]

        elif target_model == GovtBldAreaInfoModel:
            # 총괄부 표제 타입 정보
            with self.session_factory() as session:
                query = (
                    select(GovtBldAreaInfoModel)
                    .where(
                        func.date(GovtBldAreaInfoModel.created_at) == target_date
                        or func.date(GovtBldAreaInfoModel.updated_at) == target_date
                    )
                    .order_by(GovtBldAreaInfoModel.id)
                )
                results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_govt_bld_area_info_entity() for result in results
                ]

        return result_list
