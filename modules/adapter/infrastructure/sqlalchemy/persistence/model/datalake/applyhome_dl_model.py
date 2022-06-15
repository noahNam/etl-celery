from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import DOUBLE

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    ApplyHomeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base


class ApplyHomeModel(datalake_base):
    __tablename__ = "APPLYHOME_TB"

    # id == public_sale_details_id
    id = Column(
        "id",
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    offer_date = Column("모집공고일", String(10), nullable=True)
    notice_winner_date = Column("발표일", String(10), nullable=True)
    name = Column("주택명", String(100), nullable=True)
    area_type = Column("주택형", String(10), nullable=True)
    supply_price = Column("공급금액(최고가 기준)", Text, nullable=True)
    second_subs_amount = Column("청약금_2순위", Text, nullable=True)
    origin_address = Column("주소", Text, nullable=True)
    new_address = Column("주소_수정본", String(250), nullable=True)
    supply_household = Column("공급규모", Text, nullable=True)
    offer_notice_url = Column("모집공고주소", Text, nullable=True)
    move_in_date = Column("입주예정월", Text, nullable=True)
    contract_date = Column("계약일", Text, nullable=True)
    hompage_url = Column("홈페이지주소", Text, nullable=True)
    special_supply_date = Column("해당지역_특별공급_일정", Text, nullable=True)
    special_supply_etc_date = Column("기타지역_특별공급_일정", Text, nullable=True)
    special_etc_gyeonggi_date = Column("기타경기_특별공급_일정", Text, nullable=True)
    first_supply_date = Column("해당지역_1순위_일정", Text, nullable=True)
    first_supply_etc_date = Column("기타지역_1순위_일정", Text, nullable=True)
    first_etc_gyeonggi_date = Column("기타경기_1순위_일정", Text, nullable=True)
    second_supply_date = Column("해당지역_2순위_일정", Text, nullable=True)
    second_supply_etc_date = Column("기타지역_2순위_일정", Text, nullable=True)
    second_etc_gyeonggi_date = Column("기타경기_2순위_일정", Text, nullable=True)
    supply_area = Column("주택공급면적", Text, nullable=True)
    region = Column("지역", Text, nullable=True)
    housing_category = Column("주택구분", Text, nullable=True)
    rent_type = Column("분양/임대", Text, nullable=True)
    construct_company = Column("건설업체", Text, nullable=True)
    contact = Column("문의처", Text, nullable=True)
    subscription_date = Column("청약기간 순으로 정렬", Text, nullable=True)
    special_supply_status = Column("특별공급신청현황", Text, nullable=True)
    cmptt_rank = Column("경쟁률_1_2순위", Text, nullable=True)
    special_household = Column("특별공급_공급세대수", DOUBLE, nullable=True)
    multi_children_vol_etc_gyeonggi = Column("다자녀_가구_기타경기", BigInteger, nullable=True)
    multi_children_vol_etc = Column("다자녀_가구_기타지역", BigInteger, nullable=True)
    multi_children_household = Column("다자녀_가구_배정세대수", BigInteger, nullable=True)
    multi_children_vol = Column("다자녀_가구_해당지역", BigInteger, nullable=True)
    newlywed_vol_etc_gyeonggi = Column("신혼_부부_기타경기", DOUBLE, nullable=True)
    newlywed_vol_etc = Column("신혼_부부_기타지역", DOUBLE, nullable=True)
    newlywed_household = Column("신혼_부부_배정세대수", DOUBLE, nullable=True)
    newlywed_vol = Column("신혼_부부_해당지역", DOUBLE, nullable=True)
    first_life_vol_etc_gyeonggi = Column("생애최초_기타경기", DOUBLE, nullable=True)
    first_life_vol_etc = Column("생애최초_기타지역", DOUBLE, nullable=True)
    first_life_household = Column("생애최초_배정세대수", DOUBLE, nullable=True)
    first_life_vol = Column("생애최초_해당지역", DOUBLE, nullable=True)
    old_parent_vol_etc_gyeonggi = Column("노부모_부양_기타경기", DOUBLE, nullable=True)
    old_parent_vol_etc = Column("노부모_부양_기타지역", DOUBLE, nullable=True)
    old_parent_household = Column("노부모_부양_배정세대수", DOUBLE, nullable=True)
    old_parent_vol = Column("노부모_부양_해당지역", DOUBLE, nullable=True)
    agency_recommend_etc_gyeonggi = Column("기관_추천_기타경기", Text, nullable=True)
    agency_recommend_etc = Column("기관_추천_기타지역", Text, nullable=True)
    agency_recommend_house_hold = Column("기관_추천_배정세대수", Text, nullable=True)
    agency_recommend_vol = Column("기관_추천_해당지역", Text, nullable=True)
    official_general_household = Column("일반공급_공급세대수", Integer, nullable=True)
    general_household = Column("일반공급_실질_공급세대수", Integer, nullable=True)
    first_accept_cnt = Column("접수건수_1순위당해", Integer, nullable=True)
    first_accept_cnt_gyeonggi = Column("접수건수_1순위경기", Integer, nullable=True)
    first_accept_cnt_etc = Column("접수건수_1순위기타", Integer, nullable=True)
    second_accept_cnt = Column("접수건수_2순위당해", Integer, nullable=True)
    second_accept_cnt_gyeonggi = Column("접수건수_2순위경기", Integer, nullable=True)
    second_accept_cnt_etc = Column("접수건수_2순위기타", Integer, nullable=True)
    first_cmptt_rate = Column("순위내경쟁률_1순위당해", Text, nullable=True)
    first_cmptt_rate_gyeonggi = Column("순위내경쟁률_1순위경기", Text, nullable=True)
    first_cmptt_rate_etc = Column("순위내경쟁률_1순위기타", Text, nullable=True)
    second_cmptt_rate = Column("순위내경쟁률_2순위당해", Text, nullable=True)
    second_cmptt_rate_gyeonggi = Column("순위내경쟁률_2순위경기", Text, nullable=True)
    second_cmptt_rate_etc = Column("순위내경쟁률_2순위기타", Text, nullable=True)
    lowest_win_point = Column("해당지역_당첨가점최저", Text, nullable=True)
    lowest_win_point_gyeonggi = Column("기타경기_당첨가점최저", BigInteger, nullable=True)
    lowest_win_point_etc = Column("기타지역_당첨가점최저", Text, nullable=True)
    top_win_point = Column("해당지역_당첨가점최고", Text, nullable=True)
    top_win_point_gyeonggi = Column("기타경기_당첨가점최고", BigInteger, nullable=True)
    top_win_point_etc = Column("기타지역_당첨가점최고", Text, nullable=True)
    avg_win_point = Column("해당지역_당첨가점평균", Text, nullable=True)
    avg_win_point_gyeonggi = Column("기타경기_당첨가점평균", DOUBLE, nullable=True)
    avg_win_point_etc = Column("기타지역_당첨가점평균", Text, nullable=True)

    def to_apply_home_entity(self) -> ApplyHomeEntity:
        return ApplyHomeEntity(
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
