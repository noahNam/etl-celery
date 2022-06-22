from typing import Type
from sqlalchemy import exc, select

from core.domain.warehouse.bld_deal.interface.bld_deal_repository import BldDealRepository
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.bld_deal_entity import AptDealEntity, AptRentEntity, \
    OfctlDealEntity, OfctlRentEntity, RightLotOutEntity
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_detail_model import \
    PrivateSaleDetailModel

from modules.adapter.infrastructure.utils.log_helper import logger_

from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_deal_model import AptDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.apt_rent_model import AptRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_deal_model import OfctlDealModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.ofctl_rent_model import OfctlRentModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.warehouse.right_lot_out_model import RightLotOutModel

logger = logger_.getLogger(__name__)


class SyncBldDealRepository(BldDealRepository):
    def save_all(self,
                 models: list[AptDealModel] | list[AptRentModel] | list[OfctlDealModel] | list[OfctlRentModel] | list[RightLotOutModel]
                 ) -> None:
        if not models:
            return None

        try:
            session.add_all(models)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncBldDealRepository][save][{type(models[0])}] updated_at : {models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def find_to_update(
            self,
            target_model: Type[AptDealModel | AptRentModel | OfctlDealModel | OfctlRentModel | RightLotOutModel],
    ) -> list[AptDealEntity | AptRentEntity | OfctlDealEntity | OfctlRentEntity | RightLotOutEntity] | None:
        result_list = None

        query = select(target_model).where(
            target_model.update_needed == True,
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

    # def change_update_needed_status(self, value: PrivateSaleDetailModel):
    #     try:
    #         if isinstance(value, PrivateSaleDetailModel):
    #             session.execute(
    #                 update(BasicInfoModel)
    #                     .where(BasicInfoModel.house_id == value.id)
    #                     .values(
    #                     update_needed=False,
    #                 )
    #             )
    #
    #         session.commit()
    #     except exc.IntegrityError as e:
    #         logger.error(
    #             f"[SyncBldDealRepository] change_update_needed_status -> {type(value)} error : {e}"
    #         )
    #         session.rollback()