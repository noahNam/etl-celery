from typing import Callable, ContextManager
from sqlalchemy.orm import Session
from sqlalchemy import exc, update
from exceptions.base import NotUniqueErrorException

from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from core.domain.warehouse.bld_deal.interface.bld_deal_repository import BldDealsRepository

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import OfctlDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import OfctlRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel
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
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity
)

logger = logger_.getLogger(__name__)


class SyncBldDealRepository(BaseSyncRepository, BldDealsRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def save_all(self,
                 insert_models: list[AptDealModel | AptRentModel | OfctlDealModel | OfctlRentModel | RightLotOutModel],
                 ids: list[int],
                 update_model: type[GovtAptDealModel
                                    | GovtAptRentModel
                                    | GovtOfctlDealModel
                                    | GovtOfctlRentModel
                                    | GovtRightLotOutModel]
                 ) -> None:
        if not insert_models:
            return None

        with self.session_factory() as session:
            try:
                session.add_all(insert_models)
                session.execute(
                    update(update_model)
                        .where(update_model.id.in_(ids))
                        .values(
                        update_needed=False
                    )
                )
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncBuildingDealRepository][save][{type(insert_models[0])}] updated_at : {insert_models[0].updated_at} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException

    def update_supply_area(self, supply_areas: list[SupplyAreaEntity]):
        with self.session_factory() as session:
            try:
                for supply_area in supply_areas:
                    query = update(AptDealModel
                            ).where(
                                AptDealModel.house_id == supply_area.house_id
                            ).values(
                                supply_area=supply_area.supply_area,
                            )
                    session.execute(query)

                    query = update(AptRentModel
                            ).where(
                                AptRentModel.house_id == supply_area.house_id
                            ).values(
                                supply_area=supply_area.supply_area,
                            )
                    session.execute(query)

                    query = update(OfctlDealModel
                            ).where(
                                OfctlDealModel.house_id == supply_area.house_id
                            ).values(
                                supply_area=supply_area.supply_area,
                            )
                    session.execute(query)

                    query = update(OfctlRentModel
                            ).where(
                                OfctlRentModel.house_id == supply_area.house_id
                            ).values(
                                supply_area=supply_area.supply_area,
                            )
                    session.execute(query)

                    query = update(RightLotOutModel
                            ).where(
                                RightLotOutModel.house_id == supply_area.house_id
                            ).values(
                                supply_area=supply_area.supply_area,
                            )
                    session.execute(query)

                session.commit()
            except:
                session.rollback()
