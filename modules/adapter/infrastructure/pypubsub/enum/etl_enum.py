from enum import Enum


class ETLEnum(Enum):
    GET_ETL_TARGET_SCHEMAS_FROM_KAPT = "get_etl_target_schemas_from_kapt"


class TaxEnum(Enum):
    PRICE_6_AREA_85 = 0.011
    PRICE_6 = 0.013
    PRICE_9_AREA_85 = [2, 30000, 3, 0.01, 1.1]
    PRICE_9 = [2, 30000, 3, 0.01, 1.1, 0.002]
    AREA_85 = 0.033
    MAX_TAX = 0.035


class AreaRatioEnum(Enum):
    PRIVATE = [100, 0, 0]
    PUBLIC_GYEONGGI = [30, 20, 50]
    PUBLIC = [50, 0, 50]
