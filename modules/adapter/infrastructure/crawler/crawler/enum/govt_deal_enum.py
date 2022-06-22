from enum import Enum


class GovtDealEnum(Enum):
    MIN_YEAR_MONTH = "2006-01"
    MAX_YEAR_MONTH = "2022-06"
    APT_DEAL_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    APT_RENT_END_POINT = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent"
    APT_RIGHT_LOT_OUT_END_POINT = (
        "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc"
    )
    OPCTL_DEAL_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiTrade"
    OPCTL_RENT_END_POINT = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent"
    SERVICE_KEY_1 = "toLAcbnBlhSZDGMeOK8gyApaeLsaa0qrLC3urCU0k%2BtyV9%2BNA9%2FwfIYqsfF9Hi2FBcxMuJBobhGNlCAyRam%2FjQ%3D%3D"
    SERVICE_KEY_2 = "DupoKfKzoSLgBFwamlL4goP7CWP4F8e9I0OL%2Fk4lxr%2FYZrAysoaK6vlFKGVmVvqDzQrnWiFrOvlPt7FWWGHFxg%3D%3D"
    NUMBER_OF_ROWS = 1000
    DAILY_REQUEST_COUNT = 1000
