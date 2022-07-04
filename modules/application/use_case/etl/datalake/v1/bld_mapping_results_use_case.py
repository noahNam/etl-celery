from datetime import date
from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.application.use_case.etl import BaseETLUseCase

from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.govt_deals_repository import (
    SyncGovtDealRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultRepository,
)

from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    MappingGovtDetailEntity,
    MappingGovtEntity,

)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptMappingEntity,
    KaptAddrInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.legal_dong_code_entity import (
    LegalDongCodeEntity,
)

from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum

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
        kapt_repo: SyncKaptRepository,
        govt_repo: SyncGovtDealRepository,
        dong_code_repo: SyncLegalDongCodeRepository,
        bld_mapping_repo: SyncBldMappingResultRepository,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._govt_repo: SyncGovtDealRepository = govt_repo
        self._transfer: TransferBldMappingResults = TransferBldMappingResults()
        self._dong_code: SyncLegalDongCodeRepository = dong_code_repo
        self._bld_mapping_repo: SyncBldMappingResultRepository = bld_mapping_repo

    def execute(self):
        """
        1. Extract
        - legal_dong_codes
        - kapt_basic_infos (join: kapt_addr_infos, kapt_area_infos)
        - govt_apt_deals
        - govt_apt_rents
        - govt_ofctl_deals
        - govt_ofctl_rents
        - govt_right_lot_outs

        2. Transfer kapt_addr_infos
        - kapt_addr_infos에 주소코드가 있으면 사용, 없으면 생성
            - kapt_basic_infos 전처리: 주소코드, 지번 병합 및 정리

        3. Load
        - kapt_addr_infos 저장

        4. Transfer
        - 실거래가 데이터와 매핑: 주소코드, 건축년도, 지번, 아파트이름

        5. Load
        - bld_mapping_results 저장
        """

        # 1. extract
        today = date.today()

        govt_apt_deals: list[
            MappingGovtDetailEntity
        ] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value
        )

        govt_apt_rents: list[MappingGovtEntity] = self._govt_repo.find_by_update_needed(
            find_type=GovtFindTypeEnum.GOV_APT_RENT_MAPPING.value
        )

        govt_ofctl_deals = []
        # govt_ofctl_deals: list[
        #     MappingGovtEntity
        # ] = self._govt_repo.find_by_update_needed(
        #     find_type=GovtFindTypeEnum.GOV_OFCTL_DEAL_MAPPING.value
        # )

        govt_ofctl_rents = []
        # govt_ofctl_rents: list[
        #     MappingGovtEntity
        # ] = self._govt_repo.find_by_update_needed(
        #     find_type=GovtFindTypeEnum.GOV_OFCTL_RENT_MAPPING.value
        # )

        govt_right_lot_outs = []
        # govt_right_lot_outs: list[
        #     MappingGovtEntity
        # ] = self._govt_repo.find_by_update_needed(
        #     find_type=GovtFindTypeEnum.GOV_RIGHT_LOT_MAPPING.value
        # )

        kapt_basic_infos: list[KaptMappingEntity] = self._kapt_repo.find_all(
            find_type=KaptFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.value
        )

        legal_dong_codes: list[LegalDongCodeEntity] = self._dong_code.find_all()

        # 2. Transfer kapt_basic_address_codes
        func_return: [
            list[KaptMappingEntity], list[KaptAddrInfoEntity]
        ] = self._transfer.transfer_kapt_addr_infos(
            basices=kapt_basic_infos, dongs=legal_dong_codes
        )
        kapt_basic_infos = func_return[0]
        kapt_address_infos = func_return[1]

        # 3. Load
        self._kapt_repo.save_update_all(models=kapt_address_infos)

        # transfer
        bld_mapping_result_models: list[
            BldMappingResultModel
        ] = self._transfer.start_transfer(
            govt_apt_deals=govt_apt_deals,
            govt_apt_rents=govt_apt_rents,
            govt_ofctl_deals=govt_ofctl_deals,
            govt_ofctl_rents=govt_ofctl_rents,
            govt_right_lot_outs=govt_right_lot_outs,
            basices=kapt_basic_infos,
            dongs=legal_dong_codes,
            today=today,
        )

        # Load
        self._bld_mapping_repo.save_all(models=bld_mapping_result_models)
