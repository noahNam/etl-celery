from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Float,
    ForeignKey, Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)


class SubscriptionDetailModel(warehouse_base, TimestampMixin):
    __tablename__ = "subscription_details"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    subs_id = Column(
        BigInteger, ForeignKey(SubscriptionModel.subs_id), nullable=False, index=True
    )
    area_type = Column(String(10), nullable=True)
    supply_price = Column(String(10), nullable=True)
    supply_area = Column(Float, nullable=True)
    bay = Column(String(10), nullable=True)
    pansang_tower = Column(String(10), nullable=True)
    kitchen_window = Column(String(1), nullable=True)
    direct_window = Column(String(1), nullable=True)
    alpha_room = Column(String(1), nullable=True)
    special_household = Column(String(6), nullable=True)
    multi_children_vol_etc_gyeonggi = Column(String(10), nullable=True)
    multi_children_vol_etc = Column(String(10), nullable=True)
    multi_children_household = Column(String(10), nullable=True)
    multi_children_vol = Column(String(10), nullable=True)
    newlywed_vol_etc_gyeonggi = Column(String(10), nullable=True)
    newlywed_vol_etc = Column(String(10), nullable=True)
    newlywed_household = Column(String(10), nullable=True)
    newlywed_vol = Column(String(10), nullable=True)
    first_life_vol_etc_gyeonggi = Column(String(10), nullable=True)
    first_life_vol_etc = Column(String(10), nullable=True)
    first_life_household = Column(String(10), nullable=True)
    first_life_vol = Column(String(10), nullable=True)
    old_parent_vol_etc_gyeonggi = Column(String(10), nullable=True)
    old_parent_vol_etc = Column(String(10), nullable=True)
    old_parent_household = Column(String(10), nullable=True)
    old_parent_vol = Column(String(10), nullable=True)
    agency_recommend_etc_gyeonggi = Column(String(10), nullable=True)
    agency_recommend_etc = Column(String(10), nullable=True)
    agency_recommend_house_hold = Column(String(10), nullable=True)
    agency_recommend_vol = Column(String(10), nullable=True)
    official_general_household = Column(String(10), nullable=True)
    general_household = Column(String(10), nullable=True)
    first_accept_cnt = Column(String(10), nullable=True)
    first_accept_cnt_gyeonggi = Column(String(10), nullable=True)
    first_accept_cnt_etc = Column(String(10), nullable=True)
    second_accept_cnt = Column(String(10), nullable=True)
    second_accept_cnt_gyeonggi = Column(String(10), nullable=True)
    second_accept_cnt_etc = Column(String(10), nullable=True)
    first_cmptt_rate = Column(String(10), nullable=True)
    first_cmptt_rate_gyeonggi = Column(String(10), nullable=True)
    first_cmptt_rate_etc = Column(String(10), nullable=True)
    second_cmptt_rate = Column(String(10), nullable=True)
    second_cmptt_rate_gyeonggi = Column(String(10), nullable=True)
    second_cmptt_rate_etc = Column(String(10), nullable=True)
    lowest_win_point = Column(String(10), nullable=True)
    lowest_win_point_gyeonggi = Column(String(10), nullable=True)
    lowest_win_point_etc = Column(String(10), nullable=True)
    top_win_point = Column(String(10), nullable=True)
    top_win_point_gyeonggi = Column(String(10), nullable=True)
    top_win_point_etc = Column(String(10), nullable=True)
    avg_win_point = Column(String(10), nullable=True)
    avg_win_point_gyeonggi = Column(String(10), nullable=True)
    avg_win_point_etc = Column(String(10), nullable=True)
    update_needed = Column(Boolean, nullable=False, default=True)
