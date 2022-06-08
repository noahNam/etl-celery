from enum import Enum


class LegalCodeEnum(Enum):
    """
    - SERVICE_KEY(1,2...) 다수 활용 이유: 공공데이터 수집시 하루 1만건 request 제한
    - 활용처 : LegalCodeSpider
    """

    BASE_INFO_END_POINT = (
        "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
    )
    SERVICE_KEY_1 = "DupoKfKzoSLgBFwamlL4goP7CWP4F8e9I0OL%2Fk4lxr%2FYZrAysoaK6vlFKGVmVvqDzQrnWiFrOvlPt7FWWGHFxg%3D%3D"
    SERVICE_KEY_2 = "toLAcbnBlhSZDGMeOK8gyApaeLsaa0qrLC3urCU0k%2BtyV9%2BNA9%2FwfIYqsfF9Hi2FBcxMuJBobhGNlCAyRam%2FjQ%3D%3D"
    TOTAL_PAGE_NUMBER = 21
