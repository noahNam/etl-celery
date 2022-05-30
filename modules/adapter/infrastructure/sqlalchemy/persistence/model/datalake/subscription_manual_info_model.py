from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Text,
    Float,
    Numeric,
    SmallInteger,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class SubscriptionManualInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "subscription_manual_infos"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True)
    subs_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True)
    heat_type = Column(String(10), nullable=True)
    vl_rat = Column(Numeric(19, 9), nullable=True)
    bc_rat = Column(Numeric(19, 9), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    hhld_cnt = Column(SmallInteger, nullable=True)
    park_total_cnt = Column(SmallInteger, nullable=True)
    highest_floor = Column(SmallInteger, nullable=True)
    dong_cnt = Column(SmallInteger, nullable=True)
    deposit = Column(Float, nullable=True)
    middle_payment = Column(Float, nullable=True)
    balance = Column(Float, nullable=True)
    restriction_sale = Column(String(100), nullable=True)
    compulsory_residence = Column(String(100), nullable=True)
    bay = Column(String(10), nullable=True)
    pansang_tower = Column(String(10), nullable=True)
    kitchen_window = Column(String(1), nullable=True)
    direct_window = Column(String(1), nullable=True)
    alpha_room = Column(String(1), nullable=True)
    cyber_model_house_link = Column(Text, nullable=True)
    supply_rate = Column(SmallInteger, nullable=True)
    supply_rate_etc = Column(SmallInteger, nullable=True)
