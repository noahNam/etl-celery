from sqlalchemy import select, func
from datetime import date

from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
)

from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum

logger = logger_.getLogger(__name__)


class SyncGovtAptDealsRepository(BaseSyncRepository):
    def find_by_id_ls(self,
                      primary_key_ls: list[int],
                      find_type: int = 0) -> list[GovtAptDealsEntity] | None:
        """
        아파트 실거래가 데이터 가져옴
        매핑 테이블 생성에 사용
        """

        if find_type == GovtFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.value:
            with self.session_factory() as session:
                govt_apt_deals_ls = session.query(
                    GovtAptDealModel.id,
                    GovtAptDealModel.sigungu_cd,
                    GovtAptDealModel.eubmyundong_cd,
                    GovtAptDealModel.build_year,
                    GovtAptDealModel.jibun,
                    GovtAptDealModel.apt_name,
                    GovtAptDealModel.dong
                ).filter(GovtAptDealModel.id.in_(primary_key_ls)).all()

            if not govt_apt_deals_ls:
                return None
            else:
                return_ls = [govt_apt_deals.to_entity_for_bld_mapping_reuslts() for govt_apt_deals in govt_apt_deals_ls]
                return return_ls

        elif find_type == GovtFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.APT_DEALS_INPUT.value:
            pass  # fixme: 채워 넣을 것
        else:
            return None

    def find_by_date(self,
                     target_date: date,
                     find_type: int = 0) -> list[GovtAptDealsEntity] | None:
        if find_type == GovtFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtAptDealModel.id,
                    GovtAptDealModel.sigungu_cd,
                    GovtAptDealModel.eubmyundong_cd,
                    GovtAptDealModel.build_year,
                    GovtAptDealModel.jibun,
                    GovtAptDealModel.apt_name,
                    GovtAptDealModel.dong
                ).where(
                    func.date(GovtAptDealModel.created_at) == target_date
                    or func.date(GovtAptDealModel.updated_at) == target_date
                )
                govt_apt_deals_ls = session.execute(query).scalars().all()

            if not govt_apt_deals_ls:
                return None
            else:
                return_ls = [govt_apt_deals.to_entity_for_bld_mapping_reuslts() for govt_apt_deals in govt_apt_deals_ls]
                return return_ls

        elif find_type == GovtFindTypeEnum.BLD_MAPPING_RESULTS_INPUT.APT_DEALS_INPUT.value:
            pass  # fixme: 채워 넣을 것
        else:
            return None


