from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    Numeric,
    ForeignKey,
    Float,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PublicSaleModel(datamart_base, TimestampMixin):
    __tablename__ = "public_sales"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
    )
    real_estate_id = Column(
        BigInteger, ForeignKey(RealEstateModel.id), nullable=False, index=True
    )
    name = Column(String(150), nullable=True)
    region = Column(String(2), nullable=True)
    housing_category = Column(String(2), nullable=True)
    rent_type = Column(String(10), nullable=True)
    trade_type = Column(String(5), nullable=False)
    construct_company = Column(String(50), nullable=True)
    supply_household = Column(Numeric(5), nullable=True)
    offer_date = Column(String(10), nullable=True)
    subscription_start_date = Column(String(8), nullable=True)
    subscription_end_date = Column(String(8), nullable=True)
    special_supply_date = Column(String(8), nullable=True)
    special_supply_etc_date = Column(String(8), nullable=True)
    special_etc_gyeonggi_date = Column(String(8), nullable=True)
    first_supply_date = Column(String(8), nullable=True)
    first_supply_etc_date = Column(String(8), nullable=True)
    first_etc_gyeonggi_date = Column(String(8), nullable=True)
    second_supply_date = Column(String(8), nullable=True)
    second_supply_etc_date = Column(String(8), nullable=True)
    second_etc_gyeonggi_date = Column(String(8), nullable=True)
    notice_winner_date = Column(String(8), nullable=True)
    contract_start_date = Column(String(8), nullable=True)
    contract_end_date = Column(String(8), nullable=True)
    move_in_year = Column(String(4), nullable=True)
    move_in_month = Column(String(2), nullable=True)
    min_down_payment = Column(Integer, nullable=True)
    max_down_payment = Column(Integer, nullable=True)
    down_payment_ratio = Column(Integer, nullable=True)
    reference_url = Column(String(200), nullable=True)
    offer_notice_url = Column(String(100), nullable=True)
    heating_type = Column(String(10), nullable=True)
    vl_rat = Column(Numeric(6, 2), nullable=True)
    bc_rat = Column(Numeric(6, 2), nullable=True)
    hhld_total_cnt = Column(Numeric(5), nullable=True)
    park_total_cnt = Column(Numeric(5), nullable=True)
    highest_floor = Column(Numeric(3), nullable=True)
    dong_cnt = Column(Numeric(3), nullable=True)
    contact_amount = Column(Float, nullable=True)
    middle_amount = Column(Float, nullable=True)
    remain_amount = Column(Float, nullable=True)
    sale_limit = Column(String(100), nullable=True)
    compulsory_residence = Column(String(100), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    is_checked = Column(Boolean, nullable=False, default=False)
    is_available = Column(Boolean, nullable=False, default=False)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            real_estate_id=self.real_estate_id,
            name=self.name,
            region=self.region,
            housing_category=self.housing_category,
            rent_type=self.rent_type,
            trade_type=self.trade_type,
            construct_company=self.construct_company,
            supply_household=self.supply_household,
            offer_date=self.offer_date,
            subscription_start_date=self.subscription_start_date,
            subscription_end_date=self.subscription_end_date,
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
            contract_start_date=self.contract_start_date,
            contract_end_date=self.contract_end_date,
            move_in_year=self.move_in_year,
            move_in_month=self.move_in_month,
            min_down_payment=self.min_down_payment,
            max_down_payment=self.max_down_payment,
            down_payment_ratio=self.down_payment_ratio,
            reference_url=self.reference_url,
            offer_notice_url=self.offer_notice_url,
            heating_type=self.heating_type,
            vl_rat=self.vl_rat,
            bc_rat=self.bc_rat,
            hhld_total_cnt=self.hhld_total_cnt,
            park_total_cnt=self.park_total_cnt,
            highest_floor=self.highest_floor,
            dong_cnt=self.dong_cnt,
            contact_amount=self.contact_amount,
            middle_amount=self.middle_amount,
            remain_amount=self.remain_amount,
            sale_limit=self.sale_limit,
            compulsory_residence=self.compulsory_residence,
            hallway_type=self.hallway_type,
            # is_checked=self.is_checked,
            # is_available=self.is_available,
            update_needed=self.update_needed,
        )
