from enum import Enum


class GovtHouseDealEnum(Enum):
    """특정 년도, 월 범위로 범위 조정시, MIN_YEAR_MONTH, MAX_YEAR_MONTH 값 수정 후 크롤러 실행"""

    MIN_YEAR_MONTH = "2022-01"
    MAX_YEAR_MONTH = "2022-01"
    APT_DEAL_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    APT_RENT_END_POINT = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent"
    APT_RIGHT_LOT_OUT_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSilvTrade"
    OFCTL_DEAL_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiTrade"
    OFCTL_RENT_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent"
    SERVICE_KEY_1 = "DupoKfKzoSLgBFwamlL4goP7CWP4F8e9I0OL%2Fk4lxr%2FYZrAysoaK6vlFKGVmVvqDzQrnWiFrOvlPt7FWWGHFxg%3D%3D"
    SERVICE_KEY_2 = "toLAcbnBlhSZDGMeOK8gyApaeLsaa0qrLC3urCU0k%2BtyV9%2BNA9%2FwfIYqsfF9Hi2FBcxMuJBobhGNlCAyRam%2FjQ%3D%3D"
    SERVICE_KEY_3 = "gIxtryIF%2BZzKcO6VbKxvpLwwXQyT3YeCfghp5dQUQpuWoe6lxspqSNldFoxBDXlRzbI9%2FgEE4PtmPArdIz2qlw%3D%3D"
    SERVICE_KEY_4 = "vSBYKhTGXoH3QbPmk1Rlm5sg5Mlhm%2B4BkEM3F21yOUuru0gmv3oEVaDU7flRDCBhOcSLMel4P46ABHqOXXqX2A%3D%3D"
    NUMBER_OF_ROWS = 10000
    DAILY_REQUEST_COUNT = 1000000
