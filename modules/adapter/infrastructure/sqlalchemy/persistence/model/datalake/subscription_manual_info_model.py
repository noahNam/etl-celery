from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Text,
    Float,
    Numeric,
    SmallInteger,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionManualInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class SubscriptionManualInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "subscription_manual_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    subs_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    heat_type = Column(String(10), nullable=True)
    vl_rat = Column(Numeric(6, 2), nullable=True)
    bc_rat = Column(Numeric(6, 2), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    hhld_total_cnt = Column(SmallInteger, nullable=True)
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
    update_needed = Column(Boolean, nullable=False, default=False)

    def to_subs_manual_info_entity(self) -> SubscriptionManualInfoEntity:
        return SubscriptionManualInfoEntity(
            id=self.id,
            subs_id=self.subs_id,
            heat_type=self.heat_type,
            vl_rat=self.vl_rat,
            bc_rat=self.bc_rat,
            hallway_type=self.hallway_type,
            hhld_total_cnt=self.hhld_total_cnt,
            park_total_cnt=self.park_total_cnt,
            highest_floor=self.highest_floor,
            dong_cnt=self.dong_cnt,
            deposit=self.deposit,
            middle_payment=self.middle_payment,
            balance=self.balance,
            restriction_sale=self.restriction_sale,
            compulsory_residence=self.compulsory_residence,
            bay=self.bay,
            pansang_tower=self.pansang_tower,
            kitchen_window=self.kitchen_window,
            direct_window=self.direct_window,
            alpha_room=self.alpha_room,
            cyber_model_house_link=self.cyber_model_house_link,
            supply_rate=self.supply_rate,
            supply_rate_etc=self.supply_rate_etc,
        )
