from enum import Enum


class TopicEnum(Enum):
    # message pulling from redis
    SET_REDIS = "tanos.set_redis.v1"
    CRAWL_KAPT = "antgirl.crawl_kapt.v1"
    CRAWL_KAKAO_API = "antgirl.crawl_kakao_api.v1"
    ETL_WH_BASIC_INFOS = "antgirl.etl_wh_basic_infos.v1"
