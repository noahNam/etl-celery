import xmltodict


def test_xml_response_to_item():
    xml_text = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response><header><resultCode>00</resultCode>'
        "<resultMsg>NORMAL SERVICE.</resultMsg></header><body><item><codeClean>위탁관리</codeClean>"
        "<codeDisinf>위탁관리</codeDisinf><codeEcon>단일계약</codeEcon><codeElev>위탁관리</codeElev>"
        "<codeEmgr>상주선임</codeEmgr><codeFalarm>R형</codeFalarm><codeGarbage>음식물쓰레기종량제</codeGarbage>"
        "<codeMgr>위탁관리</codeMgr><codeNet>무</codeNet><codeSec>위탁관리</codeSec><codeStr>철근콘크리트구조</codeStr>"
        "<codeWsupply>부스타방식</codeWsupply>"
        "<convenientFacility>관공서(홍제1,2,3동 사무소, 홍제우체국) 병원(개구장이치과의원) 대형상가(LG하이프라자)"
        "</convenientFacility><disposalType>도포식,분무식,독이식</disposalType>"
        "<educationFacility>초등학교(인왕산, 고은, 안산, 홍제) 중학교(신연, 홍은) 고등학교(한성과학)</educationFacility>"
        "<kaptCcompany>유원종합관리(주)</kaptCcompany><kaptCode>A12009203</kaptCode><kaptMgrCnt>8</kaptMgrCnt>"
        "<kaptName>홍제무악청구1차</kaptName><kaptdCccnt>127</kaptdCccnt><kaptdClcnt>9</kaptdClcnt><kaptdDcnt>12</kaptdDcnt>"
        "<kaptdEcapa>2400</kaptdEcapa><kaptdEcnt>31</kaptdEcnt><kaptdPcnt>402</kaptdPcnt><kaptdPcntu>376</kaptdPcntu>"
        "<kaptdScnt>10</kaptdScnt><kaptdSecCom>(주)상일테크</kaptdSecCom><kaptdWtimebus>5분이내</kaptdWtimebus>"
        "<kaptdWtimesub>5분이내</kaptdWtimesub><subwayLine>3호선</subwayLine><subwayStation>홍제</subwayStation>"
        "<welfareFacility>관리사무소, 노인정, 주민공동시설, 어린이놀이터, 휴게시설, 커뮤니티공간, 자전거보관소</welfareFacility></item></body></response>"
    )
    to_dict = xmltodict.parse(xml_text)
    assert to_dict["response"]["body"]["item"].get("kaptCode") == "A12009203"
    assert to_dict["response"]["body"]["item"].get("subwayStation") == "홍제"


def test_json_response_to_item():
    pass
