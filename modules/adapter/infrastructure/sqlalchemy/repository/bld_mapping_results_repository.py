from sqlalchemy import exc
from modules.adapter.infrastructure.utils.log_helper import logger_
from exceptions.base import NotUniqueErrorException
from typing import Callable, ContextManager
from sqlalchemy.orm import Session

from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)

logger = logger_.getLogger(__name__)


class SyncBldMappingResultRepository:
    def save_all(self, models: list[BldMappingResultModel] | None) -> None:
        if not models:
            return

        try:
            session.add_all(models)
            session.commit()
            return

        except Exception as e:
            logger.error(
                f"[SyncBldMappingResultsRepository][save_all] updated_at : {models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise Exception
