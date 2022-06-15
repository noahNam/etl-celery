from sqlalchemy import Column, String, BigInteger, Integer, Text, Float

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    SubscriptionInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class SubscriptionInfoModel(datalake_base, TimestampMixin):
    __tablename__ = "subscription_infos"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    subs_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True
    )
    offer_date = Column(String(10), nullable=True)
    notice_winner_date = Column(String(10), nullable=True)
    name = Column(String(100), nullable=True)
    area_type = Column(String(10), nullable=True)
    supply_price = Column(String(10), nullable=True)
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
    supply_area = Column(Float, nullable=True)
    region = Column(String(2), nullable=True)
    housing_category = Column(String(2), nullable=True)
    rent_type = Column(String(10), nullable=True)
    construct_company = Column(String(50), nullable=True)
    contact = Column(String(25), nullable=True)
    subscription_date = Column(String(23), nullable=True)
    special_supply_status = Column(String(6), nullable=True)
    cmptt_rank = Column(String(6), nullable=True)
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

    def to_subs_info_entity(self) -> SubscriptionInfoEntity:
        return SubscriptionInfoEntity(
            id=self.id,
            offer_date=self.offer_date,
            notice_winner_date=self.notice_winner_date,
            name=self.name,
            area_type=self.area_type,
            supply_price=self.supply_price,
            second_subs_amount=self.second_subs_amount,
            origin_address=self.origin_address,
            new_address=self.new_address,
            supply_household=self.supply_household,
            offer_notice_url=self.offer_notice_url,
            move_in_date=self.move_in_date,
            contract_date=self.contract_date,
            hompage_url=self.hompage_url,
            special_supply_date=self.special_supply_date,
            special_supply_etc_date=self.special_supply_etc_date,
            special_etc_gyeonggi_date=self.special_etc_gyeonggi_date,
            first_supply_date=self.first_supply_date,
            first_supply_etc_date=self.first_supply_etc_date,
            first_etc_gyeonggi_date=self.first_etc_gyeonggi_date,
            second_supply_date=self.second_supply_date,
            second_supply_etc_date=self.second_supply_etc_date,
            second_etc_gyeonggi_date=self.second_etc_gyeonggi_date,
            supply_area=self.supply_area,
            region=self.region,
            housing_category=self.housing_category,
            rent_type=self.rent_type,
            construct_company=self.construct_company,
            contact=self.contact,
            subscription_date=self.subscription_date,
            special_supply_status=self.special_supply_status,
            cmptt_rank=self.cmptt_rank,
            special_household=self.special_household,
            multi_children_vol_etc_gyeonggi=self.multi_children_vol_etc_gyeonggi,
            multi_children_vol_etc=self.multi_children_vol_etc,
            multi_children_household=self.multi_children_household,
            multi_children_vol=self.multi_children_vol,
            newlywed_vol_etc_gyeonggi=self.newlywed_vol_etc_gyeonggi,
            newlywed_vol_etc=self.newlywed_vol_etc,
            newlywed_household=self.newlywed_household,
            newlywed_vol=self.newlywed_vol,
            first_life_vol_etc_gyeonggi=self.first_life_vol_etc_gyeonggi,
            first_life_vol_etc=self.first_life_vol_etc,
            first_life_household=self.first_life_household,
            first_life_vol=self.first_life_vol,
            old_parent_vol_etc_gyeonggi=self.old_parent_vol_etc_gyeonggi,
            old_parent_vol_etc=self.old_parent_vol_etc,
            old_parent_household=self.old_parent_household,
            old_parent_vol=self.old_parent_vol,
            agency_recommend_etc_gyeonggi=self.agency_recommend_etc_gyeonggi,
            agency_recommend_etc=self.agency_recommend_etc,
            agency_recommend_house_hold=self.agency_recommend_house_hold,
            agency_recommend_vol=self.agency_recommend_vol,
            official_general_household=self.official_general_household,
            general_household=self.general_household,
            first_accept_cnt=self.first_accept_cnt,
            first_accept_cnt_gyeonggi=self.first_accept_cnt_gyeonggi,
            first_accept_cnt_etc=self.first_accept_cnt_etc,
            second_accept_cnt=self.second_accept_cnt,
            second_accept_cnt_gyeonggi=self.second_accept_cnt_gyeonggi,
            second_accept_cnt_etc=self.second_accept_cnt_etc,
            first_cmptt_rate=self.first_cmptt_rate,
            first_cmptt_rate_gyeonggi=self.first_cmptt_rate_gyeonggi,
            first_cmptt_rate_etc=self.first_cmptt_rate_etc,
            second_cmptt_rate=self.second_cmptt_rate,
            second_cmptt_rate_gyeonggi=self.second_cmptt_rate_gyeonggi,
            second_cmptt_rate_etc=self.second_cmptt_rate_etc,
            lowest_win_point=self.lowest_win_point,
            lowest_win_point_gyeonggi=self.lowest_win_point_gyeonggi,
            lowest_win_point_etc=self.lowest_win_point_etc,
            top_win_point=self.top_win_point,
            top_win_point_gyeonggi=self.top_win_point_gyeonggi,
            top_win_point_etc=self.top_win_point_etc,
            avg_win_point=self.avg_win_point,
            avg_win_point_gyeonggi=self.avg_win_point_gyeonggi,
            avg_win_point_etc=self.avg_win_point_etc,
        )
