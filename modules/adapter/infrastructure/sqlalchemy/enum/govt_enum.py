from enum import Enum


class GovtFindTypeEnum(Enum):
    """Entity 구분용 Enum"""

    # Data Lake
    GOV_APT_DEAL_MAPPING = 0
    GOV_APT_RENT_MAPPING = 1
    GOV_OFCTL_DEAL_MAPPING = 2
    GOV_OFCTL_RENT_MAPPING = 3
    GOV_RIGHT_LOT_MAPPING = 4

    # Data Warehouse
    APT_DEALS_INPUT = 11
