from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    SmallInteger,
)
from sqlalchemy.dialects.mysql import DOUBLE

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.subs_entity import (
    GoogleSheetApplyHomeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.mapper import datalake_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class GoogleSheetApplyHomeModel(datalake_base, TimestampMixin):
    __tablename__ = "GOOGLE_SHEET_APPLYHOME_TB"

    # id == public_sale_details_id
    id = Column(
        "id",
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    # subs_id == public_sale_id
    subs_id = Column(
        "house_id",
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=True,
    )
    heating_type = Column("난방", String(100), nullable=True)
    floor_area_ratio = Column("용적률", String(10), nullable=True)
    building_cover_ratio = Column("건페율", DOUBLE(), nullable=True)
    hallway_type = Column("복도", String(3), nullable=True)
    total_household = Column("총세대수", Integer, nullable=True)
    total_park_number = Column("주차대수", Integer, nullable=True)
    top_floor = Column("최고층", SmallInteger, nullable=True)
    dong_number = Column("동수", Integer, nullable=True)
    contract_amount = Column("계약금", DOUBLE(), nullable=True)
    middle_amount = Column("중도금", DOUBLE(), nullable=True)
    remain_amount = Column("잔금", DOUBLE(), nullable=True)
    sale_limit = Column("전매제한", String(100), nullable=True)
    compulsory_residence = Column("의무거주", String(100), nullable=True)
    bay = Column("bay", SmallInteger, nullable=True)
    plate_tower_duplex = Column("판상_타워_복층", String(2), nullable=True)
    kitchen_window = Column("주방창문", String(1), nullable=True)
    cross_ventilation = Column("맞통풍", String(1), nullable=True)
    alpha_room = Column("알파룸", String(1), nullable=True)
    cyber_house_link = Column("사이버모델하우스_링크", String(200), nullable=True)
    supply_rate = Column("당해지역공급비율", SmallInteger, nullable=True)
    supply_rate_etc = Column("기타지역공급비율", SmallInteger, nullable=True)

    def to_google_sheet_apply_home_entity(self) -> GoogleSheetApplyHomeEntity:
        return GoogleSheetApplyHomeEntity(
            id=self.id,
            subs_id=self.subs_id,
            heating_type=self.heating_type,
            floor_area_ratio=self.floor_area_ratio,
            building_cover_ratio=self.building_cover_ratio,
            hallway_type=self.hallway_type,
            total_household=self.total_household,
            total_park_number=self.total_park_number,
            top_floor=self.top_floor,
            dong_number=self.dong_number,
            contract_amount=self.contract_amount,
            middle_amount=self.middle_amount,
            remain_amount=self.remain_amount,
            sale_limit=self.sale_limit,
            compulsory_residence=self.compulsory_residence,
            bay=self.bay,
            plate_tower_duplex=self.plate_tower_duplex,
            kitchen_window=self.kitchen_window,
            cross_ventilation=self.cross_ventilation,
            alpha_room=self.alpha_room,
            cyber_house_link=self.cyber_house_link,
            supply_rate=self.supply_rate,
            supply_rate_etc=self.supply_rate_etc,
        )
