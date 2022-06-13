from typing import Type

from pydantic import BaseModel
from sqlalchemy import select

from core.domain.datalake.call_failure_history.interface.call_failure_history_repository import (
    CallFailureHistoryRepository,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository


class SyncFailureRepository(CallFailureHistoryRepository, BaseSyncRepository):
    def save(self, fail_orm: CallFailureHistoryModel) -> None:
        """fail_orm : any sqlalchemy datalake_base model"""
        if not fail_orm:
            return None

        with self.session_factory() as session:
            session.add(fail_orm)
            session.commit()

        return None

    def find_by_id(self, fail_id: int) -> Type[BaseModel] | None:
        with self.session_factory() as session:
            failure_info = session.get(CallFailureHistoryModel, fail_id)

        if not failure_info:
            return None

        return failure_info.to_entity()

    def is_exists(self, fail_orm: CallFailureHistoryModel | None) -> bool:
        with self.session_factory() as session:
            if fail_orm:
                query = (
                    select(CallFailureHistoryModel)
                    .filter_by(
                        id=fail_orm.id,
                        ref_id=fail_orm.ref_id,
                        ref_table=fail_orm.ref_table,
                        reason=fail_orm.reason,
                        param=fail_orm.param,
                    )
                    .limit(1)
                )
                result = session.execute(query).scalars().first()

        if result:
            return True
        return False
