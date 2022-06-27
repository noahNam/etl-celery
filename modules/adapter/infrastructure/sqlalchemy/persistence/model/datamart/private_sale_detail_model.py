from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    Numeric,
    ForeignKey,
    Boolean,
)

from modules.adapter.infrastructure.sqlalchemy.mapper import datamart_base
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.mixins.timestamp_mixin import (
    TimestampMixin,
)


class PrivateSaleDetailModel(datamart_base, TimestampMixin):
    __tablename__ = "private_sale_details"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    private_sale_id = Column(
        BigInteger, ForeignKey(PrivateSaleModel.id), nullable=False, index=True
    )
    private_area = Column(Numeric(6, 2), nullable=True)
    supply_area = Column(Numeric(6, 2), nullable=True)
    contract_date = Column(String(8), nullable=True)
    contract_ym = Column(Numeric(6), nullable=True, index=True)
    deposit_price = Column(Integer, nullable=True)
    rent_price = Column(Integer, nullable=True)
    trade_price = Column(Integer, nullable=True, index=True)
    floor = Column(Numeric(3), nullable=True)
    trade_type = Column(String(5), nullable=False)
    is_available = Column(Boolean, nullable=False)
    update_needed = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(
            id=self.id,
            private_sale_id=self.private_sale_id,
            private_area=self.private_area,
            supply_area=self.supply_area,
            contract_date=self.contract_date,
            contract_ym=self.contract_ym,
            deposit_price=self.deposit_price,
            rent_price=self.rent_price,
            trade_price=self.trade_price,
            floor=self.floor,
            trade_type=self.trade_type,
            is_available=self.is_available,
        )