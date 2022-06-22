from sqlalchemy import exc, select, update

from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.dong_info_model import (
    DongInfoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.private_sale_model import (
    PrivateSaleModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.type_info_model import (
    TypeInfoModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncPrivateSaleRepository:
    def save(self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel) -> None:
        try:
            session.add(value)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncPrivateSaleRepository][save] target_model {type(value)} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def update(self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel) -> None:
        if isinstance(value, PrivateSaleModel):
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

    def exists_by_key(
        self, value: PrivateSaleModel | DongInfoModel | TypeInfoModel
    ) -> bool:
        result = None
        if isinstance(value, PrivateSaleModel):
            query = select(PrivateSaleModel.id).where(PrivateSaleModel.id == value.id)
            result = session.execute(query).scalars().first()

        elif isinstance(value, DongInfoModel):
            query = select(DongInfoModel.id).where(DongInfoModel.id == value.id)
            result = session.execute(query).scalars().first()

        elif isinstance(value, TypeInfoModel):
            query = select(TypeInfoModel.id).where(TypeInfoModel.id == value.id)
            result = session.execute(query).scalars().first()

        if result:
            return True

        return False
