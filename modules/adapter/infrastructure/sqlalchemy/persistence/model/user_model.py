from sqlalchemy import Column, BigInteger, Integer, String, Boolean

from modules.adapter.infrastructure.sqlalchemy.entity.user_entity import UserEntity
from modules.adapter.infrastructure.sqlalchemy.mapper import Base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class UserModel(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), primary_key=True, nullable=False
    )
    email = Column(String(75), nullable=True)
    is_required_agree_terms = Column(Boolean, nullable=False, default=False)
    join_date = Column(String(8), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_out = Column(Boolean, nullable=False, default=False)
    number_ticket = Column(Integer, nullable=False, default=0)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            is_required_agree_terms=self.is_required_agree_terms,
            join_date=self.join_date,
            is_active=self.is_active,
            is_out=self.is_out,
            number_ticket=self.number_ticket,
        )
