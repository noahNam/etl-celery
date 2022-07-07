from scrapy import Spider, Request
from scrapy.http import TextResponse, Response
from xmltodict import parse

from modules.adapter.infrastructure.crawler.crawler.enum.govt_deal_enum import (
    GovtHouseDealEnum,
)
from modules.adapter.infrastructure.crawler.crawler.items import (
    GovtHouseDealInputInfo,
    GovtAptDealInfoItem,
    GovtAptRentInfoItem,
    GovtOfctlDealInfoItem,
    GovtOfctlRentInfoItem,
    GovtRightLotOutInfoItem,
)
from modules.adapter.infrastructure.pypubsub.enum.call_failure_history_enum import (
    CallFailureTopicEnum,
)
from modules.adapter.infrastructure.pypubsub.event_listener import event_listener_dict
from modules.adapter.infrastructure.pypubsub.event_observer import send_message
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.call_failure_history_model import (
    CallFailureHistoryModel,
)


class GovtDateCounter:
    def __init__(self):
        self._min_year: int = int(GovtHouseDealEnum.MIN_YEAR_MONTH.value.split("-")[0])
        self._min_month: int = int(GovtHouseDealEnum.MIN_YEAR_MONTH.value.split("-")[1])
        self._max_year: int = int(GovtHouseDealEnum.MAX_YEAR_MONTH.value.split("-")[0])
        self._max_month: int = int(GovtHouseDealEnum.MAX_YEAR_MONTH.value.split("-")[1])
        self._current_year: int = self._min_year
        self._current_month: int = self._min_month

    def current_ym(self) -> str:
        if 0 < self._current_month < 10:
            return str(self._current_year) + "0" + str(self._current_month)
        else:
            return str(self._current_year) + str(self._current_month)

    def _is_countable_year(self) -> bool:
        if self._current_year >= self._max_year:
            return False
        return True

    def _is_countable_month(self) -> bool:
        if not self._is_countable_year() and self._current_month < self._max_month:
            return True
        if self._is_countable_year() and self._current_month < 12:
            return True
        return False

    def _plus_year(self) -> int:
        self._current_year += 1
        return self._current_year

    def plus_month(self) -> str:
        if 0 < self._current_month < 12:
            self._current_month += 1
        else:
            self._plus_year()
            self._current_month = 1
        return self.current_ym()

    def reset_counter(self) -> None:
        self._current_year: int = self._min_year
        self._current_month: int = self._min_month

    def get_max_ym(self) -> str:
        if 0 < self._max_month < 10:
            return str(self._max_year) + "0" + str(self._max_month)
        else:
            return str(self._max_year) + str(self._max_month)


class GovtHouseDealSpider(Spider):
    """현재 일일 request 횟수가 1000건 제한이기 때문에, 한번에 모든 년도 크롤링 불가능"""

    name = "govt_house_deal_infos"
    custom_settings = {
        "ITEM_PIPELINES": {
            "modules.adapter.infrastructure.crawler.crawler.pipelines.GovtHouseDealPipeline": 300
        },
    }
    open_api_service_key = GovtHouseDealEnum.SERVICE_KEY_1.value
    request_count: int = 0
    date_counter: GovtDateCounter = GovtDateCounter()

    def start_requests(self):
        """self.params: list[LegalDongCodeEntity] from GovtDealUseCase class"""
        urls: list = [
            GovtHouseDealEnum.APT_DEAL_END_POINT.value,
            GovtHouseDealEnum.APT_RENT_END_POINT.value,
            GovtHouseDealEnum.OFCTL_DEAL_END_POINT.value,
            GovtHouseDealEnum.OFCTL_RENT_END_POINT.value,
            GovtHouseDealEnum.APT_RIGHT_LOT_OUT_END_POINT.value,
        ]

        # 법정동 코드 앞 5자리 추출
        input_params: list[GovtHouseDealInputInfo] | None = self.get_input_infos(
            deal_info_list=self.params
        )

        if input_params:
            # param: 추출된 법정동 코드 앞 5자리(277개)
            for param in input_params:
                # current_ym: 200601 ~ 202206 (기간 조정시 GovtHouseDealEnum - MIN, MAX 값 조정)
                while (
                    GovtHouseDealSpider.date_counter.current_ym()
                    <= GovtHouseDealSpider.date_counter.get_max_ym()
                ):
                    yield Request(
                        url=urls[0]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_apt_deal_info,
                        errback=self.error_callback_apt_deal_info,
                        meta={
                            "url": urls[0]
                            + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                            f"&LAWD_CD={param.bjd_front_code}"
                            f"&pageNo=1"
                            f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                            f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    yield Request(
                        url=urls[1]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_apt_rent_info,
                        errback=self.error_callback_apt_rent_info,
                        meta={
                            "url": urls[1]
                            + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                            f"&LAWD_CD={param.bjd_front_code}"
                            f"&pageNo=1"
                            f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                            f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    yield Request(
                        url=urls[2]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_ofctl_deal_info,
                        errback=self.error_callback_ofctl_deal_info,
                        meta={
                            "url": urls[2]
                            + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                            f"&LAWD_CD={param.bjd_front_code}"
                            f"&pageNo=1"
                            f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                            f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    yield Request(
                        url=urls[3]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_ofctl_rent_info,
                        errback=self.error_callback_ofctl_rent_info,
                        meta={
                            "url": urls[3]
                            + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                            f"&LAWD_CD={param.bjd_front_code}"
                            f"&pageNo=1"
                            f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                            f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    yield Request(
                        url=urls[4]
                        + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                        f"&LAWD_CD={param.bjd_front_code}"
                        f"&pageNo=1"
                        f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                        f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                        callback=self.parse_apt_right_lot_out_info,
                        errback=self.error_callback_apt_right_lot_out_info,
                        meta={
                            "url": urls[4]
                            + f"?ServiceKey={GovtHouseDealSpider.open_api_service_key}"
                            f"&LAWD_CD={param.bjd_front_code}"
                            f"&pageNo=1"
                            f"&numOfRows={GovtHouseDealEnum.NUMBER_OF_ROWS.value}"
                            f"&DEAL_YMD={GovtHouseDealSpider.date_counter.current_ym()}",
                            "bjd_front_code": param,
                            "year_month": GovtHouseDealSpider.date_counter.current_ym(),
                        },
                    )

                    GovtHouseDealSpider.date_counter.plus_month()
                GovtHouseDealSpider.date_counter.reset_counter()

    def parse_apt_deal_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtAptDealInfoItem | None = None

        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                # 결과가 다수인 경우
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item = GovtAptDealInfoItem(
                        deal_amount=int(elm.get("거래금액").replace(",", ""))
                        if elm.get("거래금액")
                        else None,
                        build_year=elm.get("건축년도"),
                        deal_year=elm.get("년"),
                        road_name=elm.get("도로명"),
                        road_name_bonbun=elm.get("도로명건물본번호코드"),
                        road_name_bubun=elm.get("도로명건물부번호코드"),
                        road_name_sigungu_cd=elm.get("도로명시군구코드"),
                        road_name_seq=elm.get("도로명일련번호코드"),
                        road_name_basement_cd=elm.get("도로명지상지하코드"),
                        road_name_cd=elm.get("도로명코드"),
                        dong=elm.get("법정동"),
                        bonbun_cd=elm.get("법정동본번코드"),
                        bubun_cd=elm.get("법정동부번코드"),
                        sigungu_cd=elm.get("법정동시군구코드"),
                        eubmyundong_cd=elm.get("법정동읍면동코드"),
                        land_cd=elm.get("법정동지번코드"),
                        apt_name=elm.get("아파트"),
                        deal_month=elm.get("월"),
                        deal_day=elm.get("일"),
                        serial_no=elm.get("일련번호"),
                        exclusive_area=elm.get("전용면적"),
                        jibun=elm.get("지번"),
                        regional_cd=elm.get("지역코드"),
                        floor=elm.get("층"),
                        cancel_deal_type=elm.get("해제여부"),
                        cancel_deal_day=elm.get("해제사유발생일"),
                        req_gbn=elm.get("거래유형"),
                        rdealer_lawdnm=elm.get("중개사소재지"),
                    )

                    yield item
                return None
            elif not xml_to_dict["response"]["body"].get("items"):
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_apt_deals",
                response_or_failure=response,
            )
            return None

        try:
            # 단일 결과인 경우
            item = GovtAptDealInfoItem(
                deal_amount=int(xml_to_dict.get("거래금액").replace(",", ""))
                if xml_to_dict.get("거래금액")
                else None,
                build_year=xml_to_dict.get("건축년도"),
                deal_year=xml_to_dict.get("년"),
                road_name=xml_to_dict.get("도로명"),
                road_name_bonbun=xml_to_dict.get("도로명건물본번호코드"),
                road_name_bubun=xml_to_dict.get("도로명건물부번호코드"),
                road_name_sigungu_cd=xml_to_dict.get("도로명시군구코드"),
                road_name_seq=xml_to_dict.get("도로명일련번호코드"),
                road_name_basement_cd=xml_to_dict.get("도로명지상지하코드"),
                road_name_cd=xml_to_dict.get("도로명코드"),
                dong=xml_to_dict.get("법정동"),
                bonbun_cd=xml_to_dict.get("법정동본번코드"),
                bubun_cd=xml_to_dict.get("법정동부번코드"),
                sigungu_cd=xml_to_dict.get("법정동시군구코드"),
                eubmyundong_cd=xml_to_dict.get("법정동읍면동코드"),
                land_cd=xml_to_dict.get("법정동지번코드"),
                apt_name=xml_to_dict.get("아파트"),
                deal_month=xml_to_dict.get("월"),
                deal_day=xml_to_dict.get("일"),
                serial_no=xml_to_dict.get("일련번호"),
                exclusive_area=xml_to_dict.get("전용면적"),
                jibun=xml_to_dict.get("지번"),
                regional_cd=xml_to_dict.get("지역코드"),
                floor=xml_to_dict.get("층"),
                cancel_deal_type=xml_to_dict.get("해제여부"),
                cancel_deal_day=xml_to_dict.get("해제사유발생일"),
                req_gbn=xml_to_dict.get("거래유형"),
                rdealer_lawdnm=xml_to_dict.get("중개사소재지"),
            )
        except KeyError:
            pass

        if item:
            yield item
        else:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_apt_deals",
                response_or_failure=response,
            )
        self.count_requests()

    def parse_apt_rent_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtAptRentInfoItem | None = None

        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                # 결과가 다수인 경우
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item = GovtAptRentInfoItem(
                        build_year=elm.get("건축년도"),
                        deal_year=elm.get("년"),
                        dong=elm.get("법정동"),
                        deposit=int(elm.get("보증금액").replace(",", ""))
                        if elm.get("보증금액")
                        else None,
                        apt_name=elm.get("아파트"),
                        deal_month=elm.get("월"),
                        deal_day=elm.get("일"),
                        monthly_amount=int(elm.get("월세금액").replace(",", ""))
                        if elm.get("월세금액")
                        else None,
                        exclusive_area=elm.get("전용면적"),
                        jibun=elm.get("지번"),
                        regional_cd=elm.get("지역코드"),
                        floor=elm.get("층"),
                    )

                    yield item
                return None
            elif not xml_to_dict["response"]["body"].get("items"):
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_apt_rents",
                response_or_failure=response,
            )
            return None

        try:
            # 단일 결과인 경우
            item = GovtAptRentInfoItem(
                build_year=xml_to_dict.get("건축년도"),
                deal_year=xml_to_dict.get("년"),
                dong=xml_to_dict.get("법정동"),
                deposit=int(xml_to_dict.get("보증금액").replace(",", ""))
                if xml_to_dict.get("보증금액")
                else None,
                apt_name=xml_to_dict.get("아파트"),
                deal_month=xml_to_dict.get("월"),
                deal_day=xml_to_dict.get("일"),
                monthly_amount=int(xml_to_dict.get("월세금액").replace(",", ""))
                if xml_to_dict.get("월세금액")
                else None,
                exclusive_area=xml_to_dict.get("전용면적"),
                jibun=xml_to_dict.get("지번"),
                regional_cd=xml_to_dict.get("지역코드"),
                floor=xml_to_dict.get("층"),
            )
        except KeyError:
            pass

        if item:
            yield item
        else:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_apt_rents",
                response_or_failure=response,
            )
        self.count_requests()

    def parse_ofctl_deal_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtOfctlDealInfoItem | None = None

        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                # 결과가 다수인 경우
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item = GovtOfctlDealInfoItem(
                        deal_amount=int(elm.get("거래금액").replace(",", ""))
                        if elm.get("거래금액")
                        else None,
                        build_year=elm.get("건축년도"),
                        deal_year=elm.get("년"),
                        ofctl_name=elm.get("단지"),
                        dong=elm.get("법정동"),
                        sigungu=elm.get("시군구"),
                        deal_month=elm.get("월"),
                        deal_day=elm.get("일"),
                        exclusive_area=elm.get("전용면적"),
                        jibun=elm.get("지번"),
                        regional_cd=elm.get("지역코드"),
                        floor=elm.get("층"),
                        cancel_deal_type=elm.get("해제여부"),
                        cancel_deal_day=elm.get("해제사유발생일"),
                        req_gbn=elm.get("거래유형"),
                        rdealer_lawdnm=elm.get("중개사소재지"),
                    )

                    yield item
                return None

            elif not xml_to_dict["response"]["body"].get("items"):
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_deals",
                response_or_failure=response,
            )

        try:
            # 결과가 단일인 경우
            item = GovtOfctlDealInfoItem(
                deal_amount=int(xml_to_dict.get("거래금액").replace(",", ""))
                if xml_to_dict.get("거래금액")
                else None,
                build_year=xml_to_dict.get("건축년도"),
                deal_year=xml_to_dict.get("년"),
                ofctl_name=xml_to_dict.get("단지"),
                dong=xml_to_dict.get("법정동"),
                sigungu=xml_to_dict.get("시군구"),
                deal_month=xml_to_dict.get("월"),
                deal_day=xml_to_dict.get("일"),
                exclusive_area=xml_to_dict.get("전용면적"),
                jibun=xml_to_dict.get("지번"),
                regional_cd=xml_to_dict.get("지역코드"),
                floor=xml_to_dict.get("층"),
                cancel_deal_type=xml_to_dict.get("해제여부"),
                cancel_deal_day=xml_to_dict.get("해제사유발생일"),
                req_gbn=xml_to_dict.get("거래유형"),
                rdealer_lawdnm=xml_to_dict.get("중개사소재지"),
            )
        except KeyError:
            pass

        if item:
            yield item
        else:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_deals",
                response_or_failure=response,
            )
        self.count_requests()

    def parse_ofctl_rent_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtOfctlRentInfoItem | None = None

        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                # 결과가 다수인 경우
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item = GovtOfctlRentInfoItem(
                        deal_year=elm.get("년"),
                        ofctl_name=elm.get("단지"),
                        dong=elm.get("법정동"),
                        deposit=int(elm.get("보증금액").replace(",", ""))
                        if elm.get("보증금액")
                        else None,
                        sigungu=elm.get("시군구"),
                        deal_month=elm.get("월"),
                        deal_day=elm.get("일"),
                        monthly_amount=int(elm.get("월세금액").replace(",", ""))
                        if elm.get("월세금액")
                        else None,
                        exclusive_area=elm.get("전용면적"),
                        jibun=elm.get("지번"),
                        regional_cd=elm.get("지역코드"),
                        floor=elm.get("층"),
                    )

                    yield item
                return None
            elif not xml_to_dict["response"]["body"].get("items"):
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_rents",
                response_or_failure=response,
            )
            return None

        try:
            # 결과가 단일인 경우
            item = GovtOfctlRentInfoItem(
                deal_year=xml_to_dict.get("년"),
                ofctl_name=xml_to_dict.get("단지"),
                dong=xml_to_dict.get("법정동"),
                deposit=int(xml_to_dict.get("보증금액").replace(",", ""))
                if xml_to_dict.get("보증금액")
                else None,
                sigungu=xml_to_dict.get("시군구"),
                deal_month=xml_to_dict.get("월"),
                deal_day=xml_to_dict.get("일"),
                monthly_amount=int(xml_to_dict.get("월세금액").replace(",", ""))
                if xml_to_dict.get("월세금액")
                else None,
                exclusive_area=xml_to_dict.get("전용면적"),
                jibun=xml_to_dict.get("지번"),
                regional_cd=xml_to_dict.get("지역코드"),
                floor=xml_to_dict.get("층"),
            )
        except KeyError:
            pass

        if item:
            yield item
        else:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_rents",
                response_or_failure=response,
            )
        self.count_requests()

    def parse_apt_right_lot_out_info(self, response):
        xml_to_dict: dict = parse(response.text)
        item: GovtRightLotOutInfoItem | None = None
        try:
            if isinstance(xml_to_dict["response"]["body"]["items"]["item"], list):
                # 결과가 다수인 경우
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
                for elm in xml_to_dict:
                    item = GovtRightLotOutInfoItem(
                        deal_amount=int(elm.get("거래금액").replace(",", ""))
                        if elm.get("거래금액")
                        else None,
                        classification_owner_ship=elm.get("구분"),
                        deal_year=elm.get("년"),
                        ofctl_name=elm.get("단지"),
                        dong=elm.get("법정동"),
                        sigungu=elm.get("시군구"),
                        deal_month=elm.get("월"),
                        deal_day=elm.get("일"),
                        exclusive_area=elm.get("전용면적"),
                        jibun=elm.get("지번"),
                        regional_cd=elm.get("지역코드"),
                        floor=elm.get("층"),
                    )

                    yield item
                return None
            elif not xml_to_dict["response"]["body"].get("items"):
                item = None
            else:
                xml_to_dict = xml_to_dict["response"]["body"]["items"]["item"]
        except Exception:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_deals",
                response_or_failure=response,
            )
            return None

        try:
            # 결과가 단일인 경우
            item = GovtRightLotOutInfoItem(
                deal_amount=int(xml_to_dict.get("거래금액").replace(",", ""))
                if xml_to_dict.get("거래금액")
                else None,
                classification_owner_ship=xml_to_dict.get("구분"),
                deal_year=xml_to_dict.get("년"),
                ofctl_name=xml_to_dict.get("단지"),
                dong=xml_to_dict.get("법정동"),
                sigungu=xml_to_dict.get("시군구"),
                deal_month=xml_to_dict.get("월"),
                deal_day=xml_to_dict.get("일"),
                exclusive_area=xml_to_dict.get("전용면적"),
                jibun=xml_to_dict.get("지번"),
                regional_cd=xml_to_dict.get("지역코드"),
                floor=xml_to_dict.get("층"),
            )
        except KeyError:
            pass

        if item:
            yield item
        else:
            self.save_failure_info(
                current_url=response.request.meta.get("url"),
                bjd_front_code=response.request.meta.get("bjd_front_code"),
                year_month=response.request.meta.get("year_month"),
                ref_table="govt_ofctl_deals",
                response_or_failure=response,
            )
        self.count_requests()

    def error_callback_apt_deal_info(self, failure: Response) -> None:
        self.save_failure_info(
            current_url=failure.request.meta.get("url"),
            bjd_front_code=failure.request.meta.get("bjd_front_code"),
            year_month=failure.request.meta.get("year_month"),
            ref_table="govt_apt_deals",
            response_or_failure=failure,
        )

    def error_callback_apt_rent_info(self, failure) -> None:
        self.save_failure_info(
            current_url=failure.request.meta.get("url"),
            bjd_front_code=failure.request.meta.get("bjd_front_code"),
            year_month=failure.request.meta.get("year_month"),
            ref_table="govt_apt_rents",
            response_or_failure=failure,
        )

    def error_callback_ofctl_deal_info(self, failure) -> None:
        self.save_failure_info(
            current_url=failure.request.meta.get("url"),
            bjd_front_code=failure.request.meta.get("bjd_front_code"),
            year_month=failure.request.meta.get("year_month"),
            ref_table="govt_ofctl_deals",
            response_or_failure=failure,
        )

    def error_callback_ofctl_rent_info(self, failure) -> None:
        self.save_failure_info(
            current_url=failure.request.meta.get("url"),
            bjd_front_code=failure.request.meta.get("bjd_front_code"),
            year_month=failure.request.meta.get("year_month"),
            ref_table="govt_ofctl_rents",
            response_or_failure=failure,
        )

    def error_callback_apt_right_lot_out_info(self, failure) -> None:
        self.save_failure_info(
            current_url=failure.request.meta.get("url"),
            bjd_front_code=failure.request.meta.get("bjd_front_code"),
            year_month=failure.request.meta.get("year_month"),
            ref_table="govt_right_lot_outs",
            response_or_failure=failure,
        )

    def get_input_infos(
        self, deal_info_list: list[LegalDongCodeEntity]
    ) -> list[GovtHouseDealInputInfo]:
        extracted: list[str] = list()
        for info in deal_info_list:
            extracted.append(info.region_cd[:5])

        # 중복 제거
        duplication_removed: list[str] = list(set(extracted))

        result: list[GovtHouseDealInputInfo] = list()

        for elm in duplication_removed:
            result.append(GovtHouseDealInputInfo(bjd_front_code=elm))

        return result

    def change_service_key(self) -> None:
        if (
            GovtHouseDealSpider.open_api_service_key
            == GovtHouseDealEnum.SERVICE_KEY_2.value
        ):
            GovtHouseDealSpider.open_api_service_key = (
                GovtHouseDealEnum.SERVICE_KEY_1.value
            )
        else:
            GovtHouseDealSpider.open_api_service_key = (
                GovtHouseDealEnum.SERVICE_KEY_2.value
            )

    def count_requests(self) -> None:
        if (
            GovtHouseDealSpider.request_count
            >= GovtHouseDealEnum.DAILY_REQUEST_COUNT.value
        ):
            self.change_service_key()
            GovtHouseDealSpider.request_count = 0
        else:
            GovtHouseDealSpider.request_count += 1

    def save_failure_info(
        self,
        current_url: str,
        bjd_front_code: str,
        year_month: str,
        ref_table: str,
        response_or_failure: TextResponse | Response,
    ) -> None:
        if isinstance(response_or_failure, TextResponse):
            fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
                ref_table=ref_table,
                param=f"url: {current_url}, "
                f"current_bjd_front_code: {bjd_front_code}, "
                f"year_month: {year_month}, ",
                reason=f"response:{response_or_failure.text}",
            )
        else:
            fail_orm: CallFailureHistoryModel = CallFailureHistoryModel(
                ref_table=ref_table,
                param=f"url: {current_url}, "
                f"current_bjd_front_code: {bjd_front_code}, "
                f"year_month: {year_month}, ",
                reason=f"response:{response_or_failure}",
            )

        # if not self.__is_exists_failure(fail_orm=fail_orm):
        self.__save_crawling_failure(fail_orm=fail_orm)

    def __save_crawling_failure(self, fail_orm: CallFailureHistoryModel) -> None:
        send_message(
            topic_name=CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value,
            fail_orm=fail_orm,
        )
        event_listener_dict.get(
            f"{CallFailureTopicEnum.SAVE_CRAWLING_FAILURE.value}", None
        )

    def __is_exists_failure(self, fail_orm: CallFailureHistoryModel | None) -> bool:
        send_message(
            topic_name=CallFailureTopicEnum.IS_EXISTS.value,
            fail_orm=fail_orm,
        )
        return event_listener_dict.get(f"{CallFailureTopicEnum.IS_EXISTS.value}")
