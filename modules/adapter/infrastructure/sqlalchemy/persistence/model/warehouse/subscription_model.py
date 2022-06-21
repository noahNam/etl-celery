from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Text,
    Float,
    Numeric,
    SmallInteger, Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class SubscriptionModel(warehouse_base, TimestampMixin):
    __tablename__ = "subscriptions"

    subs_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
    )
    offer_date = Column(String(10), nullable=True)
    notice_winner_date = Column(String(10), nullable=True)
    name = Column(String(100), nullable=True)
    heat_type = Column(String(10), nullable=True)
    vl_rat = Column(Numeric(6, 2), nullable=True)
    bc_rat = Column(Numeric(6, 2), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    hhld_total_cnt = Column(Numeric(5), nullable=True)
    park_total_cnt = Column(Numeric(5), nullable=True)
    highest_floor = Column(Numeric(3), nullable=True)
    dong_cnt = Column(Numeric(5), nullable=True)
    deposit = Column(Float, nullable=True)
    middle_payment = Column(Float, nullable=True)
    balance = Column(Float, nullable=True)
    restriction_sale = Column(String(100), nullable=True)
    compulsory_residence = Column(String(100), nullable=True)
    cyber_model_house_link = Column(Text, nullable=True)
    supply_rate = Column(Numeric(3), nullable=True)
    supply_rate_etc = Column(Numeric(3), nullable=True)
    second_subs_amount = Column(String(20), nullable=True)
    origin_address = Column(String(250), nullable=True)
    new_address = Column(String(250), nullable=True)
    supply_household = Column(String(10), nullable=True)
    offer_notice_url = Column(Text, nullable=True)
    move_in_date = Column(String(10), nullable=True)
    contract_date = Column(String(23), nullable=True)
    hompage_url = Column(Text, nullable=True)
    special_supply_date = Column(String(25), nullable=True)
    special_supply_etc_date = Column(String(25), nullable=True)
    special_etc_gyeonggi_date = Column(String(25), nullable=True)
    first_supply_date = Column(String(25), nullable=True)
    first_supply_etc_date = Column(String(25), nullable=True)
    first_etc_gyeonggi_date = Column(String(25), nullable=True)
    second_supply_date = Column(String(25), nullable=True)
    second_supply_etc_date = Column(String(25), nullable=True)
    second_etc_gyeonggi_date = Column(String(25), nullable=True)
    region = Column(String(2), nullable=True)
    housing_category = Column(String(2), nullable=True)
    rent_type = Column(String(10), nullable=True)
    construct_company = Column(String(50), nullable=True)
    contact = Column(String(25), nullable=True)
    subscription_date = Column(String(23), nullable=True)
    special_supply_status = Column(String(6), nullable=True)
    cmptt_rank = Column(String(6), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)
