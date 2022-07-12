from enum import Enum


class KakaoApiEnum(Enum):
    KAKAO_PLACE_API_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query="
    KAKAO_PLACE_API_URL_NO_PARAM = "https://dapi.kakao.com/v2/local/search/keyword.json"
    KAKAO_API_KEY = "5da8fd5b2fecd850a415680330cd3524"
    KAKAO_API_KEYS = [
        "5da8fd5b2fecd850a415680330cd3524",
        "3b8170930d797a1517e33c8ed456d570",
    ]
