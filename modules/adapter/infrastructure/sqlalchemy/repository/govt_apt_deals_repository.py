from sqlalchemy import select, func
from datetime import date

from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_rent_model import (
    GovtAptRentModel
)

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_deal_model import (
    GovtOfctlDealModel
)

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_rent_model import (
    GovtOfctlRentModel
)

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_right_lot_out_model import (
    GovtRightLotOutModel
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
    GovtAptRentsEntity,
    GovtOfctlDealsEntity,
    GovtOfctlRentsEntity,
    GovtRightLotOutsEntity,
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

        if find_type == GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value:
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
                return_ls = [govt_apt_deals.to_entity_for_bld_mapping_results() for govt_apt_deals in govt_apt_deals_ls]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.APT_DEALS_INPUT.value:
            pass  # fixme: 채워 넣을 것
        else:
            return None

    def find_by_date(self,
                     target_date: date,
                     find_type: int = 0) -> list[GovtAptDealsEntity] \
                                            | list[GovtAptRentsEntity] \
                                            | list[GovtOfctlDealsEntity] \
                                            | list[GovtOfctlRentsEntity] \
                                            | list[GovtRightLotOutsEntity] | None:
        if find_type == GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value:
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
                govt_apt_deals = session.execute(query).scalars().all()

            if not govt_apt_deals:
                return None
            else:
                return_ls = [govt_apt_deal.to_entity_for_bld_mapping_results() for govt_apt_deal in govt_apt_deals]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_APT_RENT_MAPPING.value:
            with self.session_factory() as session:
                query = select(
                    GovtAptRentModel.id,
                    GovtAptRentModel.regional_cd,
                    GovtAptRentModel.dong,
                    GovtAptRentModel.build_year,
                    GovtAptRentModel.jibun,
                    GovtAptRentModel.apt_name
                ).where(
                    func.date(GovtAptRentModel.created_at) == target_date
                    or func.date(GovtAptRentModel.updated_at) == target_date
                )
                govt_apt_rents = session.execute(query).scalars().all()

            if not govt_apt_rents:
                return None
            else:
                return_ls = [govt_apt_rent.to_entity_for_bld_mapping_results() for govt_apt_rent in govt_apt_rents]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_OFCTL_DEAL_MAPPING.value:
            with self.session_factory() as session:
                query = select(
                    GovtOfctlDealModel.id,
                    GovtOfctlDealModel.regional_cd,
                    GovtOfctlDealModel.dong,
                    GovtOfctlDealModel.jibun,
                    GovtOfctlDealModel.ofctl_name
                ).where(
                    func.date(GovtOfctlDealModel.created_at) == target_date
                    or func.date(GovtOfctlDealModel.updated_at) == target_date
                )
                govt_ofctl_deals = session.execute(query).scalars().all()
            if not govt_ofctl_deals:
                return None
            else:
                return_ls = [govt_ofctl_deal.to_entity_for_bld_mapping_results() for govt_ofctl_deal in
                             govt_ofctl_deals]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_OFCTL_RENT_MAPPING.value:
            with self.session_factory() as session:
                query = select(
                    GovtOfctlRentModel.id,
                    GovtOfctlRentModel.regional_cd,
                    GovtOfctlRentModel.dong,
                    GovtOfctlRentModel.jibun,
                    GovtOfctlRentModel.ofctl_name,
                ).where(
                    func.date(GovtOfctlRentModel.created_at) == target_date
                    or func.date(GovtOfctlRentModel.updated_at) == target_date
                )
                govt_ofctl_rents = session.execute(query).scalars().all()
            if not govt_ofctl_rents:
                return None
            else:
                return_ls = [govt_ofctl_rent.to_entity_for_bld_mapping_results() for govt_ofctl_rent in
                             govt_ofctl_rents]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_RIGHT_LOT_MAPPING.value:
            with self.session_factory() as session:
                query = select(
                    GovtRightLotOutModel.id,
                    GovtRightLotOutModel.regional_cd,
                    GovtRightLotOutModel.dong,
                    GovtRightLotOutModel.jibun,
                    GovtRightLotOutModel.name
                ).where(
                    func.date(GovtRightLotOutModel.created_at) == target_date
                    or func.date(GovtRightLotOutModel.updated_at) == target_date
                )
                govt_right_lot_outs = session.execute(query).scalars().all()
            if not govt_right_lot_outs:
                return None
            else:
                return_ls = [govt_right_lot_out.to_entity_for_bld_mapping_results() for govt_right_lot_out in
                             govt_right_lot_outs]
                return return_ls

        elif find_type == GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.APT_DEALS_INPUT.value:
            pass  # fixme: 채워 넣을 것
        else:
            return None
