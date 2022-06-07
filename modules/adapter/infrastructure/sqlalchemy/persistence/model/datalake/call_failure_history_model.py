from sqlalchemy import Column, BigInteger, Integer, String, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT

from modules.adapter.infrastructure.sqlalchemy.entity.v1.call_failure_history_entity import (
    CallFailureHistoryEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class CallFailureHistoryModel(datalake_base, TimestampMixin):
    __tablename__ = "call_failure_histories"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    ref_table = Column(String(20), nullable=True)
    param = Column(String().with_variant(LONGTEXT, "mysql"), nullable=True)
    reason = Column(String().with_variant(LONGTEXT, "mysql"), nullable=True)
    is_solved = Column(Boolean, default=False)

    def to_entity(self) -> CallFailureHistoryEntity:
        return CallFailureHistoryEntity(
            id=self.id,
            ref_id=self.ref_id,
            ref_table=self.ref_table,
            reason=self.reason,
            param=self.param,
            is_solved=self.is_solved,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
