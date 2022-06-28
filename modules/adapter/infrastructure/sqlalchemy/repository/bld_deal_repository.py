from typing import Type
from sqlalchemy import exc, select, update

from core.domain.warehouse.bld_deal.interface.bld_deal_repository import (
    BldDealRepository,
)
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import (
    AptDealEntity,
    AptRentEntity,
    OfctlDealEntity,
    OfctlRentEntity,
    RightLotOutEntity,
)
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    SupplyAreaEntity,
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
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import (
    AptDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import (
    AptRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import (
    OfctlDealModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import (
    OfctlRentModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import (
    RightLotOutModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncBldDealRepository(BldDealRepository):
    def save_all(
        self,
        insert_models: list[
            AptDealModel
            | AptRentModel
            | OfctlDealModel
            | OfctlRentModel
            | RightLotOutModel
        ],
        ids: list[int],
        update_model: Type[
            GovtAptDealModel
            | GovtAptRentModel
            | GovtOfctlDealModel
            | GovtOfctlRentModel
            | GovtRightLotOutModel
        ],
    ) -> None:
        if not insert_models:
            return None

        try:
            session.add_all(insert_models)
            session.execute(
                update(update_model)
                .where(update_model.id.in_(ids))
                .values(update_needed=False)
            )
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncBuildingDealRepository][save][{type(insert_models[0])}] updated_at : {insert_models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def update_supply_area(self, supply_areas: list[SupplyAreaEntity]):
        try:
            for supply_area in supply_areas:
                query = (
                    update(AptDealModel)
                    .where(
                        AptDealModel.house_id == supply_area.house_id,
                        AptDealModel.private_area == supply_area.private_area,
                    )
                    .values(
                        supply_area=supply_area.supply_area,
                    )
                )
                session.execute(query)

                query = (
                    update(AptRentModel)
                    .where(
                        AptRentModel.house_id == supply_area.house_id,
                        AptRentModel.private_area == supply_area.private_area,
                    )
                    .values(
                        supply_area=supply_area.supply_area,
                    )
                )
                session.execute(query)

                query = (
                    update(OfctlDealModel)
                    .where(
                        OfctlDealModel.house_id == supply_area.house_id,
                        OfctlDealModel.private_area == supply_area.private_area,
                    )
                    .values(
                        supply_area=supply_area.supply_area,
                    )
                )
                session.execute(query)

                query = (
                    update(OfctlRentModel)
                    .where(
                        OfctlRentModel.house_id == supply_area.house_id,
                        OfctlRentModel.private_area == supply_area.private_area,
                    )
                    .values(
                        supply_area=supply_area.supply_area,
                    )
                )
                session.execute(query)

                query = (
                    update(RightLotOutModel)
                    .where(
                        RightLotOutModel.house_id == supply_area.house_id,
                        RightLotOutModel.private_area == supply_area.private_area,
                    )
                    .values(
                        supply_area=supply_area.supply_area,
                    )
                )
                session.execute(query)

            session.commit()

        except Exception as e:
            session.rollback()
            logger.error(
                f"[SyncBldDealRepository][update_supply_area][{type(supply_areas[0])}] house_id : {supply_areas[0].house_id} error : {e}"
            )
            session.rollback()
            raise Exception

    def find_to_update(
        self,
        target_model: Type[
            AptDealModel
            | AptRentModel
            | OfctlDealModel
            | OfctlRentModel
            | RightLotOutModel
        ],
    ) -> list[
        AptDealEntity
        | AptRentEntity
        | OfctlDealEntity
        | OfctlRentEntity
        | RightLotOutEntity
    ] | None:
        result_list = None

        query = (
            select(target_model)
            .where(
                target_model.update_needed == True,
            )
            .order_by(target_model.id)
        )
        results = session.execute(query).scalars().all()

        if results:
            if target_model == AptDealModel:
                result_list = [result.to_apt_deal_entity() for result in results]
            elif target_model == AptRentModel:
                result_list = [result.to_apt_deal_entity() for result in results]
            elif target_model == OfctlDealModel:
                result_list = [result.to_ofctl_deal_entity() for result in results]
            elif target_model == OfctlRentModel:
                result_list = [result.to_ofctl_rent_entity() for result in results]
            elif target_model == RightLotOutModel:
                result_list = [result.to_right_lot_out_entity() for result in results]

        return result_list

    def change_update_needed_status(
        self,
        target_model: AptDealEntity
        | AptRentEntity
        | OfctlDealEntity
        | OfctlRentEntity
        | RightLotOutEntity,
        update_needed_id: int,
    ):
        try:
            if isinstance(target_model, AptDealEntity):
                session.execute(
                    update(AptDealModel)
                    .where(AptDealModel.id == update_needed_id)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, AptRentEntity):
                session.execute(
                    update(AptRentModel)
                    .where(AptRentModel.id == update_needed_id)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, OfctlDealEntity):
                session.execute(
                    update(OfctlDealModel)
                    .where(OfctlDealModel.id == update_needed_id)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, OfctlRentEntity):
                session.execute(
                    update(OfctlRentModel)
                    .where(OfctlRentModel.id == update_needed_id)
                    .values(
                        update_needed=False,
                    )
                )
            elif isinstance(target_model, RightLotOutEntity):
                session.execute(
                    update(RightLotOutModel)
                    .where(RightLotOutModel.id == update_needed_id)
                    .values(
                        update_needed=False,
                    )
                )

            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncBldDealRepository] change_update_needed_status -> {target_model} error : {e}"
            )
            session.rollback()
