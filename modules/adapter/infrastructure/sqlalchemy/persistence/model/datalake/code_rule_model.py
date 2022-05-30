from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class CodeRuleModel(datalake_base, TimestampMixin):
    __tablename__ = "code_rules"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
    )
    key_div = Column(String(10), nullable=True, index=True)
    last_seq = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
