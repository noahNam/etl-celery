import os
from enum import Enum


class KakaoApiEnum(Enum):
    KAKAO_PLACE_API_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query="
    KAKAO_PLACE_API_URL_NO_PARAM = "https://dapi.kakao.com/v2/local/search/keyword.json"
    KAKAO_API_KEY = os.environ.get("KAKAO_API_KEY", "")
    KAKAO_API_KEYS = os.environ.get("KAKAO_API_KEYS", "").split(",") if os.environ.get("KAKAO_API_KEYS") else []
