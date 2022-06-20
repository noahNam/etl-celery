from enum import Enum


class GovtBldEnum(Enum):
    """
    - GOVT_BLD_TOP_URL: 총괄표제부 end_point
    - GOVT_BLD_MID_URL: 표제부 end_point
    - GOVT_BLD_AREA_URL: 전유공용면적 end_point
    - URL 1개당 일일 request 1만개 제한
    """

    GOVT_BLD_TOP_URL = (
        "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrRecapTitleInfo"
    )
    GOVT_BLD_MID_URL = "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"
    GOVT_BLD_AREA_URL = (
        "http://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo"
    )
    SERVICE_KEY_1 = "toLAcbnBlhSZDGMeOK8gyApaeLsaa0qrLC3urCU0k%2BtyV9%2BNA9%2FwfIYqsfF9Hi2FBcxMuJBobhGNlCAyRam%2FjQ%3D%3D"
    SERVICE_KEY_2 = "DupoKfKzoSLgBFwamlL4goP7CWP4F8e9I0OL%2Fk4lxr%2FYZrAysoaK6vlFKGVmVvqDzQrnWiFrOvlPt7FWWGHFxg%3D%3D"
    NUMBER_OF_ROWS = 1000
    DAILY_REQUEST_COUNT = 10000
