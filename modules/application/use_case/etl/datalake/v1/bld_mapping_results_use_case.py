from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.application.use_case.etl import BaseETLUseCase

from modules.adapter.infrastructure.sqlalchemy.repository.kakao_api_result_repository import (
    SyncKakaoApiRepository,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kakao_api_result_entity import (
    KakaoApiAddrEntity,
)
from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealRepository,
)
from modules.adapter.infrastructure.crawler.crawler.enum.govt_deal_enum import (
    GovtHouseDealEnum,
)
from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultRepository,
)
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    MappingGovtEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.apt_deal_kakao_history_model import (
    AptDealKakaoHistoryModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)
from modules.adapter.infrastructure.etl.dl_bld_mapping_reuslts import (
    TransferBldMappingResults,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)

logger = logger_.getLogger(__name__)


class BldMappingResultUseCase(BaseETLUseCase):
    def __init__(
        self,
        kakao_api_repo: SyncKakaoApiRepository,
        govt_repo: SyncGovtDealRepository,
        dong_code_repo: SyncLegalDongCodeRepository,
        bld_mapping_repo: SyncBldMappingResultRepository,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._kakao_repo: SyncKakaoApiRepository = kakao_api_repo
        self._govt_repo: SyncGovtDealRepository = govt_repo
        self._transfer: TransferBldMappingResults = TransferBldMappingResults()
        self._dong_code: SyncLegalDongCodeRepository = dong_code_repo
        self._bld_mapping_repo: SyncBldMappingResultRepository = bld_mapping_repo

    def execute(self):
        """
        1. Extract
            - govt_apt_deals
            - govt_apt_rents
            - govt_ofctl_deals
            - govt_ofctl_rents
            - govt_right_lot_outs

            - bld_mapping_results
            - legal_dong_codes

        2. Transfer
            2.1. 실거래가 데이터 & bld_mapping_results
                1) 실거래가 데이터 전처리
                    - govt_apt_deals, govt_apt_rents, govt_ofctl_deals, govt_ofctl_rents, govt_right_lot_outs 하나로 합침
                2) 검색어 중복 검사 (regoinal_cd, jibun, dong, bld_name)
                    i) 중복일 때 아무것도 안함
                    ii) 신규일 때 : kakao api request

            2.2. kakao api request
                - regoinal_cd -> 한글 이름으로 변경
                - dong
                - jibun
                - bld_name -> 괄호안 문자, 특수문자 제거

            2.2. kakao api에서 받을 결과를 kakao_api_reults 에 중복 검사
                (api에서 결과 중복, [지번주소, 빌딩이름, (도로명주소-null일때 비교 생략)])
                1) 중복되지 않을때 : 아무것도 안함
                2) 중복일 떄: bld_mapping_results 에 데이터 저장. (house_id, place_id)

            2.3. histories
                - kakao api에서 받을 결과 저장

        5. Load
        - bld_mapping_results 저장
        """
        start_year = GovtHouseDealEnum.MIN_YEAR_MONTH.value[:4]
        start_month = str(int(GovtHouseDealEnum.MIN_YEAR_MONTH.value[5:]))
        end_year = GovtHouseDealEnum.MAX_YEAR_MONTH.value[:4]
        end_month = str(int(GovtHouseDealEnum.MAX_YEAR_MONTH.value[5:]))

        # 1. extract
        # 1.1. 실거래가 데이터
        govt_apt_deals: list[MappingGovtEntity] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )

        govt_apt_rents: list[MappingGovtEntity] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_APT_RENT_MAPPING.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )

        govt_ofctl_deals: list[
            MappingGovtEntity
        ] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_OFCTL_DEAL_MAPPING.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )

        govt_ofctl_rents: list[
            MappingGovtEntity
        ] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_OFCTL_RENT_MAPPING.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )

        govt_right_lot_outs: list[
            MappingGovtEntity
        ] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_RIGHT_LOT_MAPPING.value,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )

        # kakao_api
        kakao_api_results: list[KakaoApiAddrEntity] = self._kakao_repo.find_all()

        # 1.3. 법정동 코드
        legal_dong_codes: list[LegalDongCodeEntity] = self._dong_code.find_all()

        transfered_data: [
            list[BldMappingResultModel],
            list[AptDealKakaoHistoryModel],
        ] = self._transfer.start_transfer(
            govt_apt_deals=govt_apt_deals,
            govt_apt_rents=govt_apt_rents,
            govt_ofctl_deals=govt_ofctl_deals,
            govt_ofctl_rents=govt_ofctl_rents,
            govt_right_lot_outs=govt_right_lot_outs,
            kakao_api_results=kakao_api_results,
            dongs=legal_dong_codes,
        )
        bld_mapping_results = transfered_data[0]
        apt_deal_kakao_histories = transfered_data[1]

        # Load
        self._bld_mapping_repo.save_all(
            bld_mapping_results=bld_mapping_results,
            apt_deal_kakao_histories=apt_deal_kakao_histories,
        )
