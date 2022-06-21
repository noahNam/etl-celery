from sqlalchemy import select, update
from typing import Callable, ContextManager
from sqlalchemy.orm import Session
from sqlalchemy import and_

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
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel
)

from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.govt_apt_entity import (
    GovtAptDealsEntity,
    GovtAptRentsEntity,
    GovtOfctlDealsEntity,
    GovtOfctlRentsEntity,
    GovtRightLotOutsEntity,
    GovtAptDealsJoinKeyEntity,
    GovtAptRentsJoinKeyEntity,
    GovtOfctlDealJoinKeyEntity,
    GovtOfctlRentJoinKeyEntity,
    GovtRightLotOutJoinKeyEntity
)

from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from core.domain.datalake.govt_deal.interface.govt_deal_repository import GovtDealsRepository

from modules.adapter.infrastructure.sqlalchemy.enum.govt_enum import GovtFindTypeEnum

logger = logger_.getLogger(__name__)


class SyncGovtDealsRepository(BaseSyncRepository, GovtDealsRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def find_by_update_needed(self,
                              find_type: int = 0) -> list[GovtAptDealsEntity] \
                                            | list[GovtAptRentsEntity] \
                                            | list[GovtOfctlDealsEntity] \
                                            | list[GovtOfctlRentsEntity] \
                                            | list[GovtRightLotOutsEntity] \
                                            | list[GovtAptDealsJoinKeyEntity]\
                                            | list[GovtAptRentsJoinKeyEntity]\
                                            | list[GovtOfctlDealJoinKeyEntity]\
                                            | list[GovtOfctlRentJoinKeyEntity]\
                                            | list[GovtRightLotOutJoinKeyEntity]\
                                            | None:
        if find_type == GovtFindTypeEnum.GOV_APT_DEAL_MAPPING.value:
            with self.session_factory() as session:
                query = select(
                    GovtAptDealModel
                ).where(
                    GovtAptDealModel.update_needed == True
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
                    GovtAptRentModel
                ).where(
                   GovtAptRentModel.update_needed == True
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
                    GovtOfctlDealModel
                ).where(
                    GovtOfctlDealModel.update_needed == True
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
                    GovtOfctlRentModel
                ).where(
                    GovtOfctlRentModel.update_needed == True
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
                    GovtRightLotOutModel
                ).where(
                    GovtRightLotOutModel.update_needed == True
                )
                govt_right_lot_outs = session.execute(query).scalars().all()
            if not govt_right_lot_outs:
                return None
            else:
                return_ls = [govt_right_lot_out.to_entity_for_bld_mapping_results() for govt_right_lot_out in
                             govt_right_lot_outs]
                return return_ls

        elif find_type == GovtFindTypeEnum.APT_DEALS_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtAptDealModel
                ).join(BldMappingResultModel,
                    and_(
                        BldMappingResultModel.regional_cd == GovtAptDealModel.regional_cd,
                        BldMappingResultModel.jibun == GovtAptDealModel.jibun,
                        BldMappingResultModel.dong == GovtAptDealModel.dong,
                        BldMappingResultModel.bld_name == GovtAptDealModel.apt_name
                    )
                ).where(
                    GovtAptDealModel.update_needed == True
                )
                govt_apt_deals = session.execute(query).scalars().all()

            if not govt_apt_deals:
                return None
            else:
                return_ls = [govt_apt_deal.to_entity_for_apt_deals() for govt_apt_deal in govt_apt_deals]
                return return_ls

        elif find_type == GovtFindTypeEnum.APT_RENTS_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtAptRentModel
                ).join(BldMappingResultModel,
                    and_(
                        BldMappingResultModel.regional_cd == GovtAptRentModel.regional_cd,
                        BldMappingResultModel.jibun == GovtAptRentModel.jibun,
                        BldMappingResultModel.dong == GovtAptRentModel.dong,
                        BldMappingResultModel.bld_name == GovtAptRentModel.apt_name
                    )
                ).where(
                     GovtAptRentModel.update_needed == True
                )
                govt_apt_rents = session.execute(query).scalars().all()

            if not govt_apt_rents:
                return None
            else:
                return_ls = [govt_apt_rent.to_entity_for_apt_rents() for govt_apt_rent in govt_apt_rents]
                return return_ls

        elif find_type == GovtFindTypeEnum.OFCTL_DEAL_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtOfctlDealModel
                ).join(
                    BldMappingResultModel,
                    and_(
                        BldMappingResultModel.regional_cd == GovtOfctlDealModel.regional_cd,
                        BldMappingResultModel.jibun == GovtOfctlDealModel.jibun,
                        BldMappingResultModel.dong == GovtOfctlDealModel.dong,
                        BldMappingResultModel.bld_name == GovtOfctlDealModel.ofctl_name
                    )
                ).where(
                    GovtOfctlDealModel.update_needed == True
                )
                govt_ofctl_deals = session.execute(query).scalars().all()

            if not govt_ofctl_deals:
                return None
            else:
                return_ls = [ovt_ofctl_deal.to_entity_for_ofctl_deals() for ovt_ofctl_deal in govt_ofctl_deals]
                return return_ls

        elif find_type == GovtFindTypeEnum.OFCTL_RENT_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtOfctlRentModel
                ).join(BldMappingResultModel,
                    and_(
                        BldMappingResultModel.regional_cd == GovtOfctlRentModel.regional_cd,
                        BldMappingResultModel.jibun == GovtOfctlRentModel.jibun,
                        BldMappingResultModel.dong == GovtOfctlRentModel.dong,
                        BldMappingResultModel.bld_name == GovtOfctlRentModel.ofctl_name
                    )
                ).where(
                    GovtOfctlRentModel.update_needed == True
                )
                govt_ofctl_rents = session.execute(query).scalars().all()
            if not govt_ofctl_rents:
                return None
            else:
                return_ls = [govt_ofctl_rent.to_entity_for_ofctl_rents() for govt_ofctl_rent in govt_ofctl_rents]
                return return_ls

        elif find_type == GovtFindTypeEnum.RIGHT_LOT_OUT_INPUT.value:
            with self.session_factory() as session:
                query = select(
                    GovtRightLotOutModel
                ).join(
                    BldMappingResultModel,
                    and_(
                        BldMappingResultModel.regional_cd == GovtRightLotOutModel.regional_cd,
                        BldMappingResultModel.jibun == GovtRightLotOutModel.jibun,
                        BldMappingResultModel.dong == GovtRightLotOutModel.dong,
                        BldMappingResultModel.bld_name == GovtRightLotOutModel.name
                    )
                ).where(
                    GovtRightLotOutModel.update_needed == True
                )
                govt_right_lot_outs = session.execute(query).scalars().all()
            if not govt_right_lot_outs:
                return None
            else:
                return_ls = [govt_right_lot_out.to_entity_for_right_lot_outs() for govt_right_lot_out in govt_right_lot_outs]
                return return_ls
        else:
            return None

    def alter_update_needed_by_id(self,
                                  ids: list[int],
                                  model: type[GovtAptDealModel
                                              | GovtAptRentModel
                                              | GovtOfctlDealModel
                                              | GovtOfctlRentModel
                                              | GovtRightLotOutModel],
                                  ) -> None:
        with self.session_factory() as session:
            try:
                session.execute(
                    update(model)
                        .where(model.id.in_(ids))
                        .values(
                            update_needed=False
                        )
                )
                session.commit()
            except:
                session.rollback()
