from sqlalchemy import exc, select

from core.domain.datalake.govt_house_deal.interface.govt_house_deal_repository import (
    GovtHouseDealRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.bld_mapping_result_model import (
    BldMappingResultModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_deal_model import (
    GovtAptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_apt_rent_model import (
    GovtAptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_deal_model import (
    GovtOfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_ofctl_rent_model import (
    GovtOfctlRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.govt_right_lot_out_model import (
    GovtRightLotOutModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncGovtHouseDealRepository(GovtHouseDealRepository):
    def save(
        self,
        model: GovtAptDealModel
        | GovtAptRentModel
        | GovtOfctlDealModel
        | GovtOfctlRentModel
        | GovtRightLotOutModel
        | BldMappingResultModel,
    ) -> None:
        if not model:
            return None

        try:
            session.add(model)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncGovtHouseDealRepository][save] pk: {model.id}, apt_name: {model.apt_name} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

        return None

    def is_exists(
        self,
        model: GovtAptDealModel
        | GovtAptRentModel
        | GovtOfctlDealModel
        | GovtOfctlRentModel
        | GovtRightLotOutModel
        | BldMappingResultModel,
    ) -> bool:
        result = None
        if isinstance(model, GovtAptDealModel):
            query = (
                select(GovtAptDealModel)
                .filter_by(
                    regional_cd=model.regional_cd,
                    deal_amount=model.deal_amount,
                    build_year=model.build_year,
                    deal_year=model.deal_year,
                    dong=model.dong,
                    apt_name=model.apt_name,
                    jibun=model.jibun,
                    deal_month=model.deal_month,
                    deal_day=model.deal_day,
                    serial_no=model.serial_no,
                    exclusive_area=model.exclusive_area,
                    floor=model.floor,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        elif isinstance(model, GovtAptRentModel):
            query = (
                select(GovtAptRentModel)
                .filter_by(
                    regional_cd=model.regional_cd,
                    deposit=model.deposit,
                    monthly_amount=model.monthly_amount,
                    build_year=model.build_year,
                    deal_year=model.deal_year,
                    dong=model.dong,
                    apt_name=model.apt_name,
                    jibun=model.jibun,
                    deal_month=model.deal_month,
                    deal_day=model.deal_day,
                    exclusive_area=model.exclusive_area,
                    floor=model.floor,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        elif isinstance(model, GovtOfctlDealModel):
            query = (
                select(GovtOfctlDealModel)
                .filter_by(
                    regional_cd=model.regional_cd,
                    deal_amount=model.deal_amount,
                    deal_year=model.deal_year,
                    dong=model.dong,
                    ofctl_name=model.ofctl_name,
                    sigungu=model.sigungu,
                    jibun=model.jibun,
                    deal_month=model.deal_month,
                    deal_day=model.deal_day,
                    exclusive_area=model.exclusive_area,
                    floor=model.floor,
                    rdealer_lawdnm=model.rdealer_lawdnm,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        elif isinstance(model, GovtOfctlRentModel):
            query = (
                select(GovtOfctlRentModel)
                .filter_by(
                    regional_cd=model.regional_cd,
                    deposit=model.deposit,
                    monthly_amount=model.monthly_amount,
                    deal_year=model.deal_year,
                    dong=model.dong,
                    ofctl_name=model.ofctl_name,
                    sigungu=model.sigungu,
                    jibun=model.jibun,
                    deal_month=model.deal_month,
                    deal_day=model.deal_day,
                    exclusive_area=model.exclusive_area,
                    floor=model.floor,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()
        elif isinstance(model, GovtRightLotOutModel):
            query = (
                select(GovtRightLotOutModel)
                .filter_by(
                    regional_cd=model.regional_cd,
                    deal_amount=model.deal_amount,
                    classification_owner_ship=model.classification_owner_ship,
                    deal_year=model.deal_year,
                    name=model.name,
                    dong=model.dong,
                    sigungu=model.sigungu,
                    deal_month=model.deal_month,
                    deal_day=model.deal_day,
                    jibun=model.jibun,
                    exclusive_area=model.exclusive_area,
                    floor=model.floor,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()
        elif isinstance(model, BldMappingResultModel):
            query = (
                select(BldMappingResultModel)
                .filter_by(
                    house_id=model.house_id,
                    regional_cd=model.regional_cd,
                    bld_name=model.bld_name,
                    dong=model.dong,
                    jibun=model.jibun,
                )
                .limit(1)
            )
            result = session.execute(query).scalars().first()

        if result:
            return True
        return False
