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
