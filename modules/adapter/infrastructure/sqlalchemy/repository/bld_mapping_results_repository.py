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


class SyncBldMappingResultsRepository:
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def save_all(self, models: list[BldMappingResultModel] | None) -> None:
        if not models:
            return None

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