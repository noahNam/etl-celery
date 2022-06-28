from enum import Enum


class TopicEnum(Enum):
    # message pulling from redis
    SET_REDIS = "tanos.set_redis.v1"
    CRAWL_KAPT = "antgirl.crawl_kapt.v1"
    CRAWL_KAKAO_API = "antgirl.crawl_kakao_api.v1"
    CRAWL_LEGAL_DONG_CODE = "antgirl.crawl_legal_dong_code.v1"
    CRAWL_BUILDING_MANAGE = "antgirl.crawl_building_manage.v1"

    ETL_DL_SUBS_INFOS = "antgirl.etl_dl_subs_infos.v1"  # 기존 청약홈 데이터 새로운 테이블로 이관
    ETL_DL_BLD_MAPPING_RESULTS = "antgirl.elt_bld_mapping_results.v1"

    ETL_WH_BASIC_INFOS = "antgirl.etl_wh_basic_infos.v1"
    ETL_WH_SUBS_INFOS = "antgirl.etl_wh_subs_infos.v1"

    ETL_WH_APT_DEALS = "antgirl.apt_deals.v1"
    ETL_WH_APT_RENTS = "antgirl.apt_rents.v1"
    ETL_WH_OFCTL_DEALS = "antgirl.ofctl_deals.v1"
    ETL_WH_OFCTL_RENTS = "antgirl.ofctl_rents.v1"
    ETL_WH_RIGHT_LOG_OUTS = "antgirl.right_out.v1"

    ETL_WH_UPDATE_SUPPLY_AREA = "antgirl.update_supply_area"

    ETL_MART_REAL_ESTATES = "antgirl.etl_mart_real_estates.v1"
    ETL_MART_PRIVATE_SALES = "antgirl.etl_mart_private_sales.v1"
    CRAWL_GOVT_DEAL_INFOS = "antgirl.crawl_govt_deal_infos.v1"
    ETL_MART_DONG_TYPE_INFOS = "antgirl.etl_mart_dong_type_infos.v1"
    ETL_MART_PRIVATE_SALE_DETAILS = "antgirl.etl_mart_private_sale_details.v1"



