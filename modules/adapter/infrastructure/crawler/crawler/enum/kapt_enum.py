from enum import Enum


class KaptEnum(Enum):
    """
    - SERVICE_KEY(1,2...) 다수 활용 이유: 공공데이터 수집시 하루 1만건 request 제한
    - 활용처 : KaptSpider
    """
    BASE_INFO_END_POINT = (
        "http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusBassInfo"
    )
    DETAIL_INFO_END_POINT = (
        "http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusDtlInfo"
    )
    SERVICE_KEY_1 = "toLAcbnBlhSZDGMeOK8gyApaeLsaa0qrLC3urCU0k%2BtyV9%2BNA9%2FwfIYqsfF9Hi2FBcxMuJBobhGNlCAyRam%2FjQ%3D%3D"
    SERVICE_KEY_2 = "AEiId%2BBXyNgkup%2BjvB43z1s7ZlLvuGNHMHDPWHsJfPqZNPnD5mD3x5uI14ASeSbkVh%2FxwC75ackNwEdnRrGD%2Bw%3D%3D"
    DAILY_REQUEST_COUNT = 10000
