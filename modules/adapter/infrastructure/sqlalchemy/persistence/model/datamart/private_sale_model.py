from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Boolean,
    Numeric,
    ForeignKey,
    SmallInteger,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PrivateSaleModel(datamart_base, TimestampMixin):
    __tablename__ = "private_sales"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"), nullable=False, primary_key=True
    )
    real_estate_id = Column(
        BigInteger, ForeignKey(RealEstateModel.id), nullable=False, index=True
    )
    name = Column(String(50), nullable=True)
    building_type = Column(String(5), nullable=True)
    build_year = Column(String(4), nullable=True)
    move_in_date = Column(String(8), nullable=True)
    dong_cnt = Column(Numeric(5), nullable=True)
    hhld_cnt = Column(Numeric(5), nullable=True)
    heat_type = Column(String(8), nullable=True)
    hallway_type = Column(String(4), nullable=True)
    builder = Column(String(64), nullable=True)
    park_total_cnt = Column(Numeric(5), nullable=True)
    park_ground_cnt = Column(Numeric(5), nullable=True)
    park_underground_cnt = Column(Numeric(5), nullable=True)
    cctv_cnt = Column(Numeric(5), nullable=True)
    welfare = Column(String(200), nullable=True)
    vl_rat = Column(Numeric(6, 2), nullable=True)
    bc_rat = Column(Numeric(6, 2), nullable=True)
    summer_mgmt_cost = Column(SmallInteger, nullable=True)
    winter_mgmt_cost = Column(SmallInteger, nullable=True)
    avg_mgmt_cost = Column(SmallInteger, nullable=True)
    public_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    rebuild_ref_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=True)
    trade_status = Column(Numeric(1), nullable=True, default=0)
    deposit_status = Column(Numeric(1), nullable=True, default=0)
    is_available = Column(Boolean, nullable=False)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            real_estate_id=self.real_estate_id,
            name=self.name,
            building_type=self.building_type,
            build_year=self.build_year,
            move_in_date=self.move_in_date,
            dong_cnt=int(self.dong_cnt) if self.dong_cnt else None,
            hhld_cnt=int(self.hhld_cnt) if self.hhld_cnt else None,
            heat_type=self.heat_type,
            hallway_type=self.hallway_type,
            builder=self.builder,
            park_total_cnt=int(self.park_total_cnt) if self.park_total_cnt else None,
            park_ground_cnt=int(self.park_ground_cnt) if self.park_ground_cnt else None,
            park_underground_cnt=int(self.park_underground_cnt)
            if self.park_underground_cnt
            else None,
            cctv_cnt=int(self.cctv_cnt) if self.cctv_cnt else None,
            welfare=self.welfare,
            vl_rat=self.vl_rat,
            bc_rat=self.bc_rat,
            summer_mgmt_cost=self.summer_mgmt_cost,
            winter_mgmt_cost=self.winter_mgmt_cost,
            avg_mgmt_cost=self.avg_mgmt_cost,
            public_ref_id=self.public_ref_id,
            rebuild_ref_id=self.rebuild_ref_id,
            is_available=self.is_available,
        )
