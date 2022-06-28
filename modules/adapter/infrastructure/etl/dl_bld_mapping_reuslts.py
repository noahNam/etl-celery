import re
from datetime import date

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptMappingEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
    GovtAptRentsEntity,
    GovtOfctlDealsEntity,
    GovtOfctlRentsEntity,
    GovtRightLotOutsEntity,
    GovtTransferEntity,
)
from modules.adapter.infrastructure.etl import Transfer


from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)


class TransferBldMappingResults(Transfer):
    def start_transfer(
        self,
        govt_apt_deals: list[GovtAptDealsEntity],
        govt_apt_rents: list[GovtAptRentsEntity],
        govt_ofctl_deals: list[GovtOfctlDealsEntity],
        govt_ofctl_rents: list[GovtOfctlRentsEntity],
        govt_right_lot_outs: list[GovtRightLotOutsEntity],
        basices: list[KaptMappingEntity],
        dongs: list[LegalDongCodeEntity],
        today: date,
    ) -> list[BldMappingResultModel]:
        """
        input data
        - basics's columns : house_id, sido, sigungu, eubmyun, dongri, use_apr_day, origin_dong_address, name
        - govs's columns : id, sigungu_cd, eubmyundong_cd, build_year, jibun, apt_name, dong

        전처리 순서
        1. govs 전처리
            - 10자리 주소 코드 생성
        2. basics 전처리
            - 10자리 주소 코드 생성
            - 주소에서 지번 추출
        3. govs 기준으로 basics 매핑
            - 지번주소로 필터링
            - 건축년도로 필터링
            - 지번으로 필터링
            - 아파트 이름으로 필터링

        return:
        BldMappingResultsEntity's columns:  house_id, regional_cd, jibun, dong, bld_name, created_at, updated_at
        """
        # 1. govts 전처리
        govts = list()
        if govt_apt_deals:
            for govt_apt_deal in govt_apt_deals:
                address_code: str | None = self._get_address_code(
                    govt_deal=govt_apt_deal, dong_codes=None
                )
                govt_transfer_entity = GovtTransferEntity(
                    addr_code=address_code,
                    build_year=govt_apt_deal.build_year,
                    jibun=govt_apt_deal.jibun,
                    dong=govt_apt_deal.dong,
                    apt_name=govt_apt_deal.apt_name,
                )
                govts.append(govt_transfer_entity)
        if govt_apt_rents:
            for govt_apt_rent in govt_apt_rents:
                address_code: str | None = self._get_address_code(
                    govt_deal=govt_apt_rent, dong_codes=dongs
                )
                govt_transfer_entity = GovtTransferEntity(
                    addr_code=address_code,
                    build_year=govt_apt_rent.build_year,
                    jibun=govt_apt_rent.jibun,
                    dong=govt_apt_rent.dong,
                    apt_name=govt_apt_rent.apt_name,
                )
                govts.append(govt_transfer_entity)
        if govt_ofctl_deals:
            for govt_ofctl_deal in govt_ofctl_deals:
                address_code: str | None = self._get_address_code(
                    govt_deal=govt_ofctl_deal, dong_codes=dongs
                )
                govt_transfer_entity = GovtTransferEntity(
                    addr_code=address_code,
                    build_year=None,
                    jibun=govt_ofctl_deal.jibun,
                    dong=govt_ofctl_deal.dong,
                    apt_name=govt_ofctl_deal.ofctl_name,
                )
                govts.append(govt_transfer_entity)

        if govt_ofctl_rents:
            for govt_ofctl_rent in govt_ofctl_rents:
                address_code: str | None = self._get_address_code(
                    govt_deal=govt_ofctl_rent, dong_codes=dongs
                )
                govt_transfer_entity = GovtTransferEntity(
                    addr_code=address_code,
                    build_year=None,
                    jibun=govt_ofctl_rent.jibun,
                    dong=govt_ofctl_rent.dong,
                    apt_name=govt_ofctl_rent.ofctl_name,
                )
                govts.append(govt_transfer_entity)

        if govt_right_lot_outs:
            for govt_right_lot_out in govt_right_lot_outs:
                address_code: str | None = self._get_address_code(
                    govt_deal=govt_right_lot_out, dong_codes=dongs
                )
                govt_transfer_entity = GovtTransferEntity(
                    addr_code=address_code,
                    build_year=None,
                    jibun=govt_right_lot_out.jibun,
                    dong=govt_right_lot_out.dong,
                    apt_name=govt_right_lot_out.name,
                )
                govts.append(govt_transfer_entity)

        # 2. basics 전처리
        basic_adress_codes = list()
        basic_jibuns = list()
        i = 0
        for basic_entity in [basices[0]]:
            i += 1
            if i % 100 == 0:
                print(i)
            # addr_code 10자리 주소코드
            addr_code: str | None = self._get_basic_adress_code(
                sido=basic_entity.sido,
                sigungu=basic_entity.sigungu,
                eubmyun=basic_entity.eubmyun,
                dongri=basic_entity.dongri,
                dong_code_entities=dongs,
            )
            basic_adress_codes.append(addr_code)

            # 지번
            basic_jibun: str | None = self._get_jibun(
                sido=basic_entity.sido,
                sigungu=basic_entity.sigungu,
                eubmyun=basic_entity.eubmyun,
                dongri=basic_entity.dongri,
                apt_name=basic_entity.name,
                address=basic_entity.origin_dong_address,
            )
            basic_jibuns.append(basic_jibun)

        # 3. 매핑 (govs, basics)
        return_values = list()  # BldMappingResultsEntity list
        for i in range(len(govts)):
            # 1. 주소 코드 같은 apt_basic 필터링
            basic_indexes = self._filter_basices_by_addr_code(
                addr_code=govts[i].addr_code, basic_addr_codes=basic_adress_codes
            )
            # 2. 건축년도로 apt_basic 필터링
            basic_indexes = self._filter_basices_by_build_year(
                basic_indexes=basic_indexes,
                basices=basices,
                build_year=govts[i].build_year,
            )
            # 3. 지번으로 apt_basic 필터링
            basic_indexes = self._filter_basices_by_jibun(
                basic_indexes=basic_indexes,
                basic_jibuns=basic_jibuns,
                jibun=govts[i].jibun,
            )
            # 4. 아파트 이름으로 apt_basic 필터링
            basic_index = self._filter_basices_by_apt_name(
                basic_indexes=basic_indexes, basices=basices, apt_name=govts[i].apt_name
            )
            if basic_index is None:
                continue
            else:
                house_id = basices[basic_index].house_id

            model = BldMappingResultModel(
                house_id=house_id,
                regional_cd=govts[i].addr_code,
                jibun=govts[i].jibun,
                dong=govts[i].dong,  # entity 추가해야함
                bld_name=govts[i].apt_name,
                created_at=today,
                updated_at=today,
            )
            return_values.append(model)
        return return_values

    def _filter_basices_by_apt_name(
        self, basic_indexes: list[int], basices: list[KaptMappingEntity], apt_name: str
    ) -> int | None:
        return_idx = None
        for idx in basic_indexes:
            if apt_name == basices[idx].name:
                return_idx = idx
                break

        return return_idx

    def _filter_basices_by_jibun(
        self, basic_indexes: list[int], basic_jibuns: list[str], jibun: str
    ) -> list[int]:
        if jibun is None:
            return basic_indexes

        new_basic_indexes = list()
        for idx in basic_indexes:
            if jibun == basic_jibuns[idx]:
                new_basic_indexes.append(idx)
            else:
                pass
        if len(new_basic_indexes) == 0:
            return basic_indexes
        else:
            return new_basic_indexes

    def _filter_basices_by_build_year(
        self,
        basic_indexes: list[int],
        basices: list[KaptMappingEntity],
        build_year: str | None,
    ) -> list[int]:
        if build_year is None:
            return basic_indexes

        new_basic_indexes = list()
        for idx in basic_indexes:
            if int(build_year) == int(str(basices[idx].use_apr_day)[0:4]):
                new_basic_indexes.append(idx)
            else:
                pass
        return new_basic_indexes

    def _filter_basices_by_addr_code(
        self, addr_code: str, basic_addr_codes: list[str]
    ) -> list[int] | None:
        addr_8_code = addr_code[8:10] + "00"
        addr_5_code = addr_code[6:10] + "00000"

        if addr_code in basic_addr_codes:
            basic_indexes = self._find_all_index(
                value=addr_code, values=basic_addr_codes
            )
        elif addr_8_code in basic_addr_codes:
            basic_indexes = self._find_all_index(
                value=addr_8_code, values=basic_addr_codes
            )
        elif addr_5_code in basic_addr_codes:
            basic_indexes = self._find_all_index(
                value=addr_5_code, values=basic_addr_codes
            )
        else:
            return None
        return basic_indexes

    def _find_all_index(
        self, value: str | int, values: list[str] | list[int]
    ) -> list[int]:
        indexes = list()
        for i in range(len(values)):
            if values[i] == value:
                indexes.append(i)
        return indexes

    def _get_basic_adress_code(
        self,
        sido,
        sigungu,
        eubmyun,
        dongri,
        dong_code_entities: list[LegalDongCodeEntity],
    ) -> str | None:
        regexes = list()
        if sido is None or sido == "":
            return None
        if dongri is not None or dongri != "":
            regex_dongri = "".join([sido, ".*", dongri, ".*"])
            regexes.append(regex_dongri)
        if eubmyun is not None or eubmyun != "":
            regex_eubmyun = "".join([sido, ".*", eubmyun, ".*"])
            regexes.append(regex_eubmyun)
        if sigungu is not None or sigungu != "":
            regex_sigungu = "".join([sido, ".*", sigungu, ".*"])
            regexes.append(regex_sigungu)
        if len(regexes) == 0:
            return None

        code = None
        for regex in regexes:
            for dong_code_entity in dong_code_entities:
                regular_expression = re.compile(regex, re.DOTALL)
                find_result = regular_expression.search(dong_code_entity.locatadd_nm)

                if find_result is None:
                    continue
                else:
                    code = dong_code_entity.region_cd
                    return code
        return code

    def _get_jibun(
        self,
        sido: str,
        sigungu: str,
        eubmyun: str,
        dongri: str,
        apt_name: str,
        address: str,
    ) -> str | None:
        return_addr = address.replace(apt_name, "")
        return_addr = return_addr.replace(sido, "")
        return_addr = return_addr.replace(sigungu, "")
        return_addr = return_addr.replace(eubmyun, "")
        return_addr = return_addr.replace(dongri, "")
        return_addr = return_addr.replace(" ", "")
        if return_addr == "" or return_addr == "0":
            return None
        else:
            return return_addr

    def _get_address_code(
        self,
        govt_deal: GovtAptDealsEntity
        | GovtAptRentsEntity
        | GovtOfctlDealsEntity
        | GovtOfctlRentsEntity
        | GovtRightLotOutsEntity,
        dong_codes: list[LegalDongCodeEntity] | None,
    ) -> str | None:
        """
        1. GovtAptDealsEntity 인 경우 (아파트 매매 실거래가)
        - 주소코드 앞 5자리, 주소코드 뒷 5자리 합쳐서 사용

        2. 이외 실거래가
        - 주소코드 앞 5자리 그대로 사용
        - 주소코드 6번째자리 ~ 8번째 자리는 읍면동 코드. 읍면동 문자열 데이터를 변환해 사용.
        - 뒷 두자리(9~10번째 자리) 코드는 '00'으로 고정
        """
        if isinstance(govt_deal, GovtAptDealsEntity):
            sigungu_cd = govt_deal.sigungu_cd
            eubmyundong_cd = govt_deal.sigungu_cd

            if eubmyundong_cd is None:
                address_code = "".join([sigungu_cd, "00000"])
            else:
                address_code = "".join([sigungu_cd, eubmyundong_cd])

        else:
            address_code = str(govt_deal.regional_cd)
            dong = govt_deal.dong
            dong_code = "000"
            for dong_entity in dong_codes:
                # 시도, 시군구가 같은지 비교
                addr_code_5 = "".join(
                    [str(dong_entity.sido_cd), str(dong_entity.sgg_cd)]
                )
                if address_code == addr_code_5:
                    # 읍면동 비교
                    if dong in dong_entity.locatadd_nm:
                        dong_code = dong_entity.umd_cd
                        break
            address_code = "".join([address_code, dong_code, "00"])
        return address_code
