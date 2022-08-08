from typing import Type

from sqlalchemy import select, exc, and_

from core.domain.datalake.govt_bld_info.interface.govt_bld_info_repository import (
    GovtBldRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
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
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncGovtBldRepository(GovtBldRepository):
    def save(
        self,
        bld_orm: GovtBldTopInfoModel
        | GovtBldMiddleInfoModel
        | GovtBldAreaInfoModel
        | None,
    ) -> None:
        if not bld_orm:
            return None

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
        result = None
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

    def find_to_update(
        self,
        target_model: Type[
            GovtBldTopInfoModel | GovtBldMiddleInfoModel | GovtBldAreaInfoModel
        ],
    ) -> list[
        GovtBldTopInfoEntity | GovtBldMiddleInfoEntity | GovtBldAreaInfoEntity
    ] | None:
        result_list = None

        if target_model == GovtBldTopInfoModel:
            #  총괄부 표제 단지 정보
            query = (
                select(GovtBldTopInfoModel)
                .where(
                    GovtBldTopInfoModel.update_needed == True,
                )
                .order_by(
                    GovtBldTopInfoModel.house_id,
                    GovtBldTopInfoModel.new_old_regstr_gb_cd,
                )
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_govt_bld_top_info_entity() for result in results
                ]

        elif target_model == GovtBldMiddleInfoModel:
            # 총괄부 표제 동 정보
            filters = list()
            filters.append(
                and_(
                    GovtBldMiddleInfoModel.update_needed == True,
                )
            )

            query = (
                select(GovtBldMiddleInfoModel)
                .where(*filters)
                .order_by(GovtBldMiddleInfoModel.house_id)
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_govt_bld_middle_info_entity() for result in results
                ]

        elif target_model == GovtBldAreaInfoModel:
            # 총괄부 표제 타입 정보
            filters = list()
            filters.append(
                and_(
                    GovtBldAreaInfoModel.update_needed == True,
                    # house_id 일부만 필터하기
                    GovtBldAreaInfoModel.house_id >= 1511,
                    GovtBldAreaInfoModel.house_id <= 1520,
                )
                # 관련 쿼리 넣을지 확정 안됨.
                # & not_(
                #     or_(
                #         GovtBldAreaInfoModel.etc_purps.like("%주차장%"),
                #         GovtBldAreaInfoModel.etc_purps.like("%관리%"),
                #         GovtBldAreaInfoModel.etc_purps.like("%기계%"),
                #         GovtBldAreaInfoModel.etc_purps.like("%전기%"),
                #         GovtBldAreaInfoModel.etc_purps.like("%제어%"),
                #         GovtBldAreaInfoModel.etc_purps.like("%경비%"),
                #     )
                # )
            )

            query = (
                select(GovtBldAreaInfoModel)
                .where(*filters)
                .order_by(GovtBldAreaInfoModel.house_id, GovtBldAreaInfoModel.rnum)
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_govt_bld_area_info_entity() for result in results
                ]

        return result_list
