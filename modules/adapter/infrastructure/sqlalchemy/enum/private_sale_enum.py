from enum import Enum


class PrivateSaleTradeTypeEnum(Enum):
    """private_sale_details.trade_type"""

    TRADING = "매매"
    LONG_TERM_RENT = "전세"
    MONTHLY_RENT = "월세"
    PUBLIC_TRADE = "분양권매매"
    PRIVATE_TRADE = "입주권매매"
