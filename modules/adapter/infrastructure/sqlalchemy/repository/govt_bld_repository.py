from sqlalchemy import select, exc

from core.domain.datalake.govt_bld_info.interface.govt_bld_info_repository import (
    GovtBldRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_area_info_model import (
    GovtBldAreaInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_middle_info_model import (
    GovtBldMiddleInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_bld_top_info_model import (
    GovtBldTopInfoModel,
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
