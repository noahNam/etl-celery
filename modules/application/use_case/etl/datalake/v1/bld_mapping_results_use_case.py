from datetime import date
from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.application.use_case.etl import BaseEtlUseCase

from modules.adapter.infrastructure.sqlalchemy.repository.kapt_repository import (
    SyncKaptRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.govt_apt_deals_repository import (
    SyncGovtAptDealsRepository,
)

from modules.adapter.infrastructure.sqlalchemy.repository.legal_dong_code_repository import (
    SyncLegalDongCodeRepository
)

from modules.adapter.infrastructure.sqlalchemy.repository.bld_mapping_results_repository import (
    SyncBldMappingResultsRepository
)

from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
    GovtAptRentsEntity,
    GovtOfctlDealsEntity,
    GovtOfctlRentsEntity,
    GovtRightLotOutsEntity
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.kapt_entity import (
    KaptMappingEntity
)

from modules.adapter.infrastructure.sqlalchemy.enum.kapt_enum import KaptFindTypeEnum

from modules.adapter.infrastructure.etl.dl_bld_mapping_reuslts import TransferBldMappingResults

logger = logger_.getLogger(__name__)


class BldMappingResultsUseCase(BaseEtlUseCase):
    def __init__(self, kapt_repo, govt_repo, dong_code_repo, bld_mapping_repo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._kapt_repo: SyncKaptRepository = kapt_repo
        self._govt_repo: SyncGovtAptDealsRepository = govt_repo
        self._transfer: TransferBldMappingResults = TransferBldMappingResults()
        self._dong_code: SyncLegalDongCodeRepository = dong_code_repo
        self._bld_mapping_repo: SyncBldMappingResultsRepository = bld_mapping_repo

    def execute(self):
        # extract
        today = date.today()
        dong_codes = self._dong_code.find_all()

        kapt_basic_infos: list[KaptMappingEntity] = self._kapt_repo.find_by_date_and_type(
            target_date=today,
            find_type=KaptFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.value
        )

        govt_apt_deals: list[GovtAptDealsEntity] = self._govt_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value
        )

        govt_apt_rents: list[GovtAptRentsEntity] = self._govt_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.GOV_APT_RENT_MAPPING.value
        )

        govt_ofctl_deals: list[GovtOfctlDealsEntity] = self._govt_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.GOV_OFCTL_DEAL_MAPPING.value
        )

        govt_ofctl_rents: list[GovtOfctlRentsEntity] = self._govt_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.GOV_OFCTL_RENT_MAPPING.value
        )
        govt_right_lot_outs: list[GovtRightLotOutsEntity] = self._govt_repo.find_by_date(
            target_date=today,
            find_type=GovtFindTypeEnum.GOV_RIGHT_LOT_MAPPING.value
        )

        # transfer
        bld_mapping_result_models = self._transfer.start_etl(
            govt_apt_deals=govt_apt_deals,
            govt_apt_rents=govt_apt_rents,
            govt_ofctl_deals=govt_ofctl_deals,
            govt_ofctl_rents=govt_ofctl_rents,
            govt_right_lot_outs=govt_right_lot_outs,
            basices=kapt_basic_infos,
            dongs=dong_codes,
            today=today
        )

        # Load
        # result columns : place_id, house_id, regional_cd, jibun, dong, bld_name, created_at, updated_at
        self._bld_mapping_repo.save_all(bld_mapping_result_models)
