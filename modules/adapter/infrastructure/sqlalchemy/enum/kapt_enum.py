from enum import Enum


class KaptFindTypeEnum(Enum):
    """KaptRepository Entity 구분용 Enum"""

    KAPT_OPEN_API_INPUT = 0
    KAKAO_API_INPUT = 1
    BLD_MAPPING_RESULTS_INPUT = 2


class CodeRuleKeyEnum(Enum):
    """code_rules last seq 구분 key Enum"""

    HOUSE_ID = "house_id"
    SUBS_ID = "subs_id"
    PRIVATE_SALE_DETAIL_ID = "private_sale_detail_id"
