from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Float,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship

from modules.adapter.infrastructure.sqlalchemy.mapper import warehouse_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.subscription_entity import (
    SubDtToPublicDtEntity,
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

    subs = relationship(
        "SubscriptionModel",
        backref="subscription_details",
        uselist=False,
        primaryjoin="foreign(SubscriptionDetailModel.subs_id) == SubscriptionModel.subs_id",
    )

    def to_entity_for_public_sale_details(self) -> SubDtToPublicDtEntity:
        return SubDtToPublicDtEntity(
            id=self.id,
            subs_id=self.subs_id,
            area_type=self.area_type,
            supply_area=self.supply_area,
            special_household=self.special_household,
            multi_children_household=self.multi_children_household,
            newlywed_household=self.newlywed_household,
            old_parent_household=self.old_parent_household,
            first_life_household=self.first_life_household,
            general_household=self.general_household,
            bay=self.bay,
            pansang_tower=self.pansang_tower,
            kitchen_window=self.kitchen_window,
            direct_window=self.direct_window,
            alpha_room=self.alpha_room,
            cyber_model_house_link=self.subs.cyber_model_house_link,
            housing_category=self.subs.housing_category,
            region=self.subs.region,
            supply_rate=self.subs.supply_rate,
            supply_rate_etc=self.subs.supply_rate_etc,
            multi_children_vol=self.multi_children_vol,
            multi_children_vol_etc_gyeonggi=self.multi_children_vol_etc_gyeonggi,
            multi_children_vol_etc=self.multi_children_vol_etc,
            newlywed_vol=self.newlywed_vol,
            newlywed_vol_etc_gyeonggi=self.newlywed_vol_etc_gyeonggi,
            newlywed_vol_etc=self.newlywed_vol_etc,
            old_parent_vol=self.old_parent_vol,
            old_parent_vol_etc_gyeonggi=self.old_parent_vol_etc_gyeonggi,
            old_parent_vol_etc=self.old_parent_vol_etc,
            first_life_vol=self.first_life_vol,
            first_life_vol_etc_gyeonggi=self.first_life_vol_etc_gyeonggi,
            first_life_vol_etc=self.first_life_vol_etc,
            first_accept_cnt=self.first_accept_cnt,
            first_accept_cnt_gyeonggi=self.first_accept_cnt_gyeonggi,
            first_accept_cnt_etc=self.first_accept_cnt_etc,
            first_cmptt_rate=self.first_cmptt_rate,
            first_cmptt_rate_gyeonggi=self.first_cmptt_rate_gyeonggi,
            first_cmptt_rate_etc=self.first_cmptt_rate_etc,
            lowest_win_point=self.lowest_win_point,
            lowest_win_point_gyeonggi=self.lowest_win_point_gyeonggi,
            lowest_win_point_etc=self.lowest_win_point_etc,
        )
