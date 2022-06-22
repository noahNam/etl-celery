from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Text,
    Float,
    Numeric,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubsToPublicEntity
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

    def to_entity_for_public_sales(self) -> SubsToPublicEntity:
        return SubsToPublicEntity(
            name=self.name,
            region=self.region,
            housing_category=self.housing_category,
            rent_type=self.rent_type,
            construct_company=self.construct_company,
            supply_household=self.supply_household,
            offer_date=self.offer_date,
            subscription_date=self.subscription_date,
            special_supply_date=self.special_supply_date,
            special_supply_etc_date=self.special_supply_etc_date,
            special_etc_gyeonggi_date=self.special_etc_gyeonggi_date,
            first_supply_date=self.first_supply_date,
            first_supply_etc_date=self.first_supply_etc_date,
            first_etc_gyeonggi_date=self.first_etc_gyeonggi_date,
            second_supply_date=self.second_supply_date,
            second_supply_etc_date=self.second_supply_etc_date,
            second_etc_gyeonggi_date=self.second_etc_gyeonggi_date,
            notice_winner_date=self.notice_winner_date,
            contract_date=self.contract_date,
            move_in_date=self.move_in_date,
            # supply_price=self.supply_price,
            cyber_model_house_link=self.cyber_model_house_link,
            offer_notice_url=self.offer_notice_url,
            heat_type=self.heat_type,
            vl_rat=self.vl_rat,
            bc_rat=self.bc_rat,
            hhld_total_cnt=self.hhld_total_cnt,
            park_total_cnt=self.park_total_cnt,
            highest_floor=self.highest_floor,
            dong_cnt=self.dong_cnt,
            deposit=self.deposit,
            middle_payment=self.middle_payment,
            balance=self.balance,
            restriction_sale=self.restriction_sale,
            compulsory_residence=self.compulsory_residence,
            hallway_type=self.hallway_type
        )
