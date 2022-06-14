from sqlalchemy import exc
from modules.adapter.infrastructure.utils.log_helper import logger_
from exceptions.base import NotUniqueErrorException

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)

from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository

logger = logger_.getLogger(__name__)


class SyncBldMappingResultsRepository(BaseSyncRepository):
    def save_all(self, models: list[BldMappingResultModel] | None) -> None:
        if not models:
            return None

        with self.session_factory() as session:
            try:
                session.add_all(models)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncBldMappingResultsRepository][save] updated_at : {models[0].updated_at} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException
            return None

    def save(
        self,
        target_model: Type[
            BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel
        ],
        value: [BasicInfoModel | DongInfoModel | TypeInfoModel | MgmtCostModel],
    ) -> None:
        with self.session_factory() as session:
            try:
                session.add(value)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncBasicRepository][save] target_model : {target_model} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException
