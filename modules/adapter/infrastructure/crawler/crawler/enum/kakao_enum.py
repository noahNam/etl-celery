from enum import Enum


class KakaoApiEnum(Enum):
    KAKAO_PLACE_API_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query="
    KAKAO_PLACE_API_URL_NO_PARAM = "https://dapi.kakao.com/v2/local/search/keyword.json"
    KAKAO_API_KEY = "***REMOVED***"
    KAKAO_API_KEYS = [
        "***REMOVED***",
        "308910f9cd565c2d9e6b45091812f5ff",
        "16f23d61ef7bef8cbdea926f63c7f78b",
        "0ed0526c4fa4859f9adc513eed350670",
    ]
