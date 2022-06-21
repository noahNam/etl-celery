from typing import Callable, ContextManager
from sqlalchemy import exc, select, update
from sqlalchemy.orm import Session

from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import DongInfoModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_detail_model import \
    PrivateSaleDetailModel
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.type_info_model import TypeInfoModel
from modules.adapter.infrastructure.sqlalchemy.repository import BaseSyncRepository
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncPrivateSaleRepository(BaseSyncRepository):
    def __init__(self, session_factory: Callable[..., ContextManager[Session]]):
        super().__init__(session_factory=session_factory)

    def save(self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel | PrivateSaleDetailModel) -> None:
        with self.session_factory() as session:
            try:
                session.add(value)
                session.commit()
            except exc.IntegrityError as e:
                logger.error(
                    f"[SyncPrivateSaleRepository][save] target_model {type(value)} error : {e}"
                )
                session.rollback()
                raise NotUniqueErrorException

    def update(self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel | PrivateSaleDetailModel) -> None:
        if isinstance(value, PrivateSaleModel):
            with self.session_factory() as session:
                session.execute(
                    update(PrivateSaleModel)
                    .where(PrivateSaleModel.id == value.id)
                    .values(
                        real_estate_id=value.real_estate_id,
                        name=value.name,
                        building_type=value.building_type,
                        build_year=value.build_year,
                        move_in_date=value.move_in_date,
                        dong_cnt=value.dong_cnt,
                        hhld_cnt=value.hhld_cnt,
                        heat_type=value.heat_type,
                        hallway_type=value.hallway_type,
                        builder=value.builder,
                        park_total_cnt=value.park_total_cnt,
                        park_ground_cnt=value.park_ground_cnt,
                        park_underground_cnt=value.park_underground_cnt,
                        cctv_cnt=value.cctv_cnt,
                        welfare=value.welfare,
                        vl_rat=value.vl_rat,
                        bc_rat=value.bc_rat,
                        summer_mgmt_cost=value.summer_mgmt_cost,
                        winter_mgmt_cost=value.winter_mgmt_cost,
                        avg_mgmt_cost=value.avg_mgmt_cost,
                        public_ref_id=value.public_ref_id,
                        rebuild_ref_id=value.rebuild_ref_id,
                        is_available=value.is_available,
                    )
                )

                session.commit()

        elif isinstance(value, DongInfoModel):
            with self.session_factory() as session:
                session.execute(
                    update(DongInfoModel)
                    .where(DongInfoModel.id == value.id)
                    .values(
                        private_sale_id=value.private_sale_id,
                        name=value.name,
                        hhld_cnt=value.hhld_cnt,
                        grnd_flr_cnt=value.grnd_flr_cnt,
                        update_needed=value.update_needed,
                    )
                )

                session.commit()

        elif isinstance(value, TypeInfoModel):
            with self.session_factory() as session:
                session.execute(
                    update(TypeInfoModel)
                    .where(TypeInfoModel.id == value.id)
                    .values(
                        dong_id=value.dong_id,
                        private_area=value.private_area,
                        supply_area=value.supply_area,
                        update_needed=value.update_needed,
                    )
                )

                session.commit()

        elif isinstance(value, PrivateSaleDetailModel):
            with self.session_factory() as session:
                session.execute(
                    update(PrivateSaleDetailModel)
                    .where(PrivateSaleDetailModel.id == value.id)
                    .values(
                        private_sale_id=value.private_sale_id,
                        private_area=value.private_area,
                        supply_area=value.supply_area,
                        contract_date=value.contract_date,
                        contract_ym=value.contract_ym,
                        deposit_price=value.deposit_price,
                        rent_price=value.rent_price,
                        trade_price=value.trade_price,
                        floor=value.floor,
                        trade_type=value.trade_type,
                        is_available=value.is_available,
                        update_needed=value.update_needed,
                    )
                )

                session.commit()

    def exists_by_key(self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel | PrivateSaleDetailModel) -> bool:
        if isinstance(value, PrivateSaleModel):
            with self.session_factory() as session:
                query = select(PrivateSaleModel.id).where(PrivateSaleModel.id == value.id)
                result = session.execute(query).scalars().first()

        elif isinstance(value, DongInfoModel):
            with self.session_factory() as session:
                query = select(DongInfoModel.id).where(DongInfoModel.id == value.id)
                result = session.execute(query).scalars().first()

        elif isinstance(value, TypeInfoModel):
            with self.session_factory() as session:
                query = select(TypeInfoModel.id).where(TypeInfoModel.id == value.id)
                result = session.execute(query).scalars().first()

        elif isinstance(value, PrivateSaleDetailModel):
            with self.session_factory() as session:
                query = select(PrivateSaleDetailModel.id).where(PrivateSaleDetailModel.id == value.id)
                result = session.execute(query).scalars().first()

        if result:
            return True

        return False
