from enum import Enum


class SubscriptionInfoEnum(Enum):
    """
    - START_YEAR_MONTH, END_YEAR_MONTH : yyyy년 mm월 형식으로 입력
    - START_YEAR_MONTH ~ END_YEAR_MONTH 기간 차이 : 청약홈 제약상 최대 12개월만 가능합니다
    - ex) 2021년 08월 ~ 2022년 07월
    """

    START_YEAR_MONTH = "2022년 06월"
    END_YEAR_MONTH = "2022년 06월"
    APPLY_HOME_URL = (
        "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do"
    )
