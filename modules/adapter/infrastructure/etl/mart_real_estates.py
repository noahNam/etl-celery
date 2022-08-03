from typing import Any
import re
from tqdm import tqdm

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiResultEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.subscription_model import (
    SubscriptionModel,
)

class TransformRealEstate:
    def start_etl(
        self,
        basic_infos: list[BasicInfoEntity],
        kakao_api_results: list[KakaoApiResultEntity],
        legal_dong_codes: list[LegalDongCodeEntity],
    ) -> list[Any] | None:
        real_estates = list()
        if not basic_infos:
            pass
        elif isinstance(basic_infos[0], BasicInfoEntity):
            real_estates_basic = self._etl_basic_infos(target_list=basic_infos)
            real_estates.extend(real_estates_basic)

        if not kakao_api_results:
            pass
        elif isinstance(kakao_api_results[0], KakaoApiResultEntity):
            real_estates_kakao = self._etl_kakao_api_results(
                target_list=kakao_api_results,
                legal_dong_codes=legal_dong_codes
            )
            real_estates.extend(real_estates_kakao)

        return real_estates

    def _etl_basic_infos(
        self, target_list: list[BasicInfoEntity]
    ) -> list[RealEstateModel]:
        result = list()
        for target_entity in tqdm(target_list):
            if not target_entity.place_id:
                continue

            result.append(
                RealEstateModel(
                    id=target_entity.place_id,
                    name=target_entity.bld_name,
                    jibun_address=target_entity.place_dong_address,
                    road_address=target_entity.place_road_address,
                    si_do=target_entity.sido,
                    si_gun_gu=target_entity.sigungu,
                    dong_myun=target_entity.dongri + " " + target_entity.eubmyun,
                    road_name=target_entity.road_name,
                    road_number=target_entity.road_number,
                    land_number=target_entity.land_number,
                    x_vl=target_entity.x_vl,
                    y_vl=target_entity.y_vl,
                    front_legal_code=target_entity.sigungu_cd,
                    back_legal_code=target_entity.bjdong_cd,
                    is_available=target_entity.is_available,
                    update_needed=True,
                )
            )
        return result

    def _etl_kakao_api_results(
        self,
        target_list: list[KakaoApiResultEntity],
        legal_dong_codes: list[LegalDongCodeEntity],
    ) -> list[RealEstateModel]:

        result = list()
        for target_entity in target_list:
            if not target_entity:
                continue

            if not target_entity.id and target_entity.jibun_address:
                continue

            address_segments: list[str] = target_entity.jibun_address.split()
            sido: str | None = address_segments[0]
            sigungu: str | None = self.__get_address_segment(
                address_segments=address_segments[1:], search_type='sigungu'
            )
            eubmyun: str | None = self.__get_address_segment(
                address_segments=address_segments[1:], search_type='eubmyun'
            )
            dong: str | None = self.__get_address_segment(
                address_segments=address_segments[1:], search_type='dong'
            )
            ri: str | None = self.__get_address_segment(
                address_segments=address_segments[1:], search_type='ri'
            )
            land_number: str | None = self.__get_address_number(
                address_segments=address_segments[1:]
            )

            if target_entity.road_address:
                road_address_segments = target_entity.road_address.split()
                road_number = self.__get_address_number(
                    address_segments=road_address_segments
                )
                if road_number:
                    road_name = target_entity.road_address.replace(road_number, "")
                    if road_name[-1] == " ":
                        road_name = road_name[:-1]

                else:
                    road_name = target_entity.road_address
            else:
                road_name = None
                road_number = None

            legal_codes: dict | None = self.__get_front_legal_code(
                sido=sido,
                sigungu=sigungu,
                eubmyun=eubmyun,
                dong=dong,
                ri=ri,
                legal_dong_codes=legal_dong_codes,
            )

            if not eubmyun and not dong:
                dong_myun = None
            elif not eubmyun:
                dong_myun = dong
            elif not dong:
                dong_myun = eubmyun
            else:
                dong_myun = " ".join([dong, eubmyun])

            result.append(
                RealEstateModel(
                    id=target_entity.id,
                    name=target_entity.bld_name,
                    jibun_address=target_entity.jibun_address,
                    road_address=target_entity.road_address,
                    si_do=sido,
                    si_gun_gu=sigungu,
                    dong_myun=dong_myun,
                    road_name=road_name,
                    road_number=road_number,
                    land_number=land_number,
                    x_vl=target_entity.x_vl,
                    y_vl=target_entity.y_vl,
                    front_legal_code=legal_codes.get("front_legal_code"),
                    back_legal_code=legal_codes.get("back_legal_code"),
                    is_available=True,
                    update_needed=True,
                )
            )
        return result

    def __get_address_segment(
            self,
            address_segments: list[str],
            search_type: str
    ) -> str | None:
        if search_type == 'sigungu':
            search_filter = ['시', '군', '구']
        elif search_type == 'eubmyun':
            search_filter = ['읍', '면']
        elif search_type == "dong":
            search_filter = ['동']
        elif search_type == 'ri':
            search_filter = ['리']
        else:
            return None

        si_gun_gu = ''
        for seg in address_segments:
            if seg[-1:] in search_filter:
                if si_gun_gu == '':
                    si_gun_gu = seg
                else:
                    si_gun_gu = ' '.join([si_gun_gu, seg])
        return si_gun_gu

    def __get_address_number(
            self,
            address_segments: list
    ) -> str | None:
        land_number = address_segments[-1]
        if land_number.replace("-", "").isdigit():
            return land_number
        else:
            return None

    def __get_front_legal_code(
            self,
            sido: str,
            sigungu: str,
            eubmyun: str,
            dong: str,
            ri: str,
            legal_dong_codes: list[LegalDongCodeEntity],
    ) -> dict:
        if not sido or not sigungu:
            return dict(
                front_legal_code=None,
                back_legal_code=None,
            )

        patterns = list()
        if ri:
            dongri = ri
        elif dong:
            dongri = dong
        else:
            dongri = None

        if dongri and not eubmyun:
            patterns.append(
                "".join([sido, ".*", dongri, ".*"])
            )

        if eubmyun and not dongri:
            patterns.append(
                "".join([sido, ".*", eubmyun, ".*"])
            )

        if dongri and eubmyun:
            patterns.append(
                "".join(
                    [
                        sido,
                        ".*",
                        eubmyun,
                        ".*",
                        dongri,
                        ".*",
                    ]
                )
            )

        if not patterns:
            return dict(
                front_legal_code=None,
                back_legal_code=None,
            )

        for pattern in patterns:
            for legal_dong_code in legal_dong_codes:
                regex = re.compile(pattern, re.DOTALL)
                find_result = regex.search(legal_dong_code.locatadd_nm)

                if find_result:
                    return dict(
                        front_legal_code=legal_dong_code.region_cd[:5],
                        back_legal_code=legal_dong_code.region_cd[5:],
                    )
        return dict(
            front_legal_code=None,
            back_legal_code=None,
        )

    def get_place_id(
            self,
            subscriptions: list[SubscriptionModel],
    ) -> list[int | None]:
        return_list = list()

        for subscription in subscriptions:
            return_list.append(subscription.place_id)
        return return_list
