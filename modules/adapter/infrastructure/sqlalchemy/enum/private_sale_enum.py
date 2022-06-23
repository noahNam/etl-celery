from enum import Enum


class PrivateSaleTradeTypeEnum(Enum):
    """private_sale_details.trade_type"""

    TRADING = "매매"
    PUBLIC_TRADE = "분양권매매"
    RENT_TRADE = "임대매매"
    LONG_TERM_RENT = "전세"
    MONTHLY_RENT = "월세"
    PRIVATE_TRADE = "입주권매매"


# PrivateSaleTradeTypeEnum
