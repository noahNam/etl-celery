import requests
from tqdm import tqdm

from modules.adapter.infrastructure.crawler.crawler.enum.kakao_enum import KakaoApiEnum
from modules.adapter.infrastructure.utils.log_helper import (
    logger_,
    TqdmLoggingHandler
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    MappingGovtEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiAddrEntity,
)
from modules.adapter.infrastructure.etl import Transfer
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.apt_deal_kakao_history_model import (
    AptDealKakaoHistoryModel
)

logger = logger_.getLogger(__name__)
logger.addHandler(TqdmLoggingHandler())


class TransferBldMappingResults(Transfer):
    def start_transfer(
        self,
        govt_apt_deals: list[MappingGovtEntity],
        govt_apt_rents: list[MappingGovtEntity],
        govt_ofctl_deals: list[MappingGovtEntity],
        govt_ofctl_rents: list[MappingGovtEntity],
        govt_right_lot_outs: list[MappingGovtEntity],
        kakao_api_results: list[KakaoApiAddrEntity],
        dongs: list[LegalDongCodeEntity],
    ) -> [list[BldMappingResultModel], list[AptDealKakaoHistoryModel]]:
        """
        2.1. 실거래가 데이터 & bld_mapping_results : 검색어 중복 검사 (검색어 중복 [jibun, dong, bld_name, regoinal_cd])
            1) 중복일 때 아무것도 안함
            2) 신규일 때 : kakao api request
        """

        # govts 전처리
        govts: list[MappingGovtEntity] = (
                govt_apt_deals + govt_apt_rents + govt_ofctl_deals + govt_ofctl_rents + govt_right_lot_outs
        )
        new_govts: list[MappingGovtEntity] = list()
        for govt in tqdm(govts, desc="new_govts", mininterval=1):
            if not govt.mapping_id and govt.regional_cd and govt.apt_name:  # mapping_id가 없는 것들만 작업
                new_govts.append(govt)

        if not new_govts:
            return [[], []]
        # new_govts = new_govts[:2]
        # kakao api에 보낼 주소 전처리
        govt_addresses: list[str] = list()
        for govt in tqdm(new_govts, desc="govt_addresses", mininterval=1):
            sido_ymm = self._get_addr(regional_cd=govt.regional_cd, dongs=dongs)
            dong = govt.dong if govt.dong else ''
            jibun = govt.jibun if govt.jibun else ''
            apt_name = govt.apt_name if govt.apt_name else ''
            address = ' '.join([sido_ymm, dong, jibun, apt_name])
            govt_addresses.append(address)

        # kakao api request
        kakao_addresses = list()
        kakao_key_number: int = self._get_kakao_key_usable_number()
        for i in tqdm(range(len(new_govts)), desc="kakao_addresses", mininterval=1):
            try:
                response = self._request_kakao_api(
                    address=govt_addresses[i], key_number=kakao_key_number
                )
                if response in [429, 401]:
                    kakao_key_number = self._get_kakao_key_usable_number()

                    response = self._request_kakao_api(
                        address=govt_addresses[i], key_number=kakao_key_number
                    )
                kakao_addresses.append(response)
            except Exception as e:
                break


        # 1. kakao_api_results 테이블에 같은 것이 있는지 찾기
        # 2. 같은것이 있으면 bld_mapping_reuslts 에 쌓기
        # 3. history 데이터 정리
        apt_deal_kakao_histories = list()
        bld_mapping_results = list()
        for i in tqdm(range(len(kakao_addresses)), desc="bld_mapping_results", mininterval=1):
            # 1. place_id (매핑되었을 때 값 불러옴)
            mapping_ids: list[int] = self._get_mapping_key(
                response=kakao_addresses[i], kakao_api_results=kakao_api_results
            )

            kakao_api_results_id = mapping_ids[0]
            house_id = mapping_ids[1]
            if not house_id:
                continue

            # 2. bld_mapping_result Entity 세팅
            if kakao_api_results_id:
                bld_mapping_result = BldMappingResultModel(
                    house_id=house_id,
                    place_id=kakao_api_results_id,
                    regional_cd=new_govts[i].regional_cd,
                    jibun=new_govts[i].jibun,
                    dong=new_govts[i].dong,
                    bld_name=new_govts[i].apt_name,
                )
                bld_mapping_results.append(bld_mapping_result)
            # 3. history 데이터 정리

            if not kakao_addresses[i]:
                x_vl = None
                y_vl = None
                jibun_address = None
                bld_name = None
            else:
                x_vl = kakao_addresses[i]["x"]
                y_vl = kakao_addresses[i]["y"]
                jibun_address = kakao_addresses[i]["address_name"]
                bld_name = kakao_addresses[i]["place_name"]

            apt_deal_kakao_history = AptDealKakaoHistoryModel(
                regional_cd=new_govts[i].regional_cd,
                sido_sigungu=govt_addresses[i],
                dong=new_govts[i].dong,
                jibun=new_govts[i].jibun,
                search_apt_name=new_govts[i].apt_name,
                x_vl=x_vl,
                y_vl=y_vl,
                jibun_address=jibun_address,
                bld_name=bld_name,
            )
            apt_deal_kakao_histories.append(apt_deal_kakao_history)
        return [bld_mapping_results, apt_deal_kakao_histories]

    def _get_addr(self, regional_cd: str | None, dongs: list[LegalDongCodeEntity]) -> str:
        if not regional_cd:
            return ''

        for dong in dongs:
            if ''.join([regional_cd,'00000']) == dong.region_cd:
                locatadd_nm = dong.locatadd_nm if dong.locatadd_nm else ''
                return locatadd_nm
        return ''

    def _request_kakao_api(
            self, address: str, key_number: int
    ) -> dict | None | int:
        url: str = KakaoApiEnum.KAKAO_PLACE_API_URL_NO_PARAM.value
        headers: dict = {
            "Authorization": f"KakaoAK {KakaoApiEnum.KAKAO_API_KEYS.value[key_number]}"
        }
        params = {
            "query": "{}".format(address)
        }
        res = requests.get(url=url, params=params, headers=headers)

        # kakao 응답에 문제가 있는지 확인
        if res.status_code in [429, 401]:
            return res.status_code
        else:
            kakao_addresses = res.json()['documents']
            if not kakao_addresses:
                return None

            kakao_address = None
            for addr in kakao_addresses:
                if '아파트' in addr['category_name'] and '아파트상가' not in addr['category_name']:
                    kakao_address = addr
                    break

            return kakao_address

    def _get_kakao_key_usable_number(self) -> int:
        test_address = "서울 강남구 광평로10길 15"
        all_key_cnt = len(KakaoApiEnum.KAKAO_API_KEYS.value)
        key_idx = None
        for i in range(all_key_cnt):
            res = self._request_kakao_api(address=test_address, key_number=i)
            if res != 429:
                return i

        if not key_idx:
            raise Exception('kakao API limit has been exceeded')

    def _get_mapping_key(
            self,
            response: dict,
            kakao_api_results: list[KakaoApiAddrEntity]
    ) -> list[int | None]:
        for kakao_api_result in kakao_api_results:
            if not response:
                return [None, None]

            if (response["address_name"] == kakao_api_result.jibun_address and
                    response["place_name"] == kakao_api_result.bld_name):
                if not response["road_address_name"]:
                    return [kakao_api_result.id, kakao_api_result.house_id]
                elif response["road_address_name"] == kakao_api_result.road_address:
                    return [kakao_api_result.id, kakao_api_result.house_id]
        return [None, None]
