from sqlalchemy import update, exc
from sqlalchemy.future import select

from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)
from modules.adapter.infrastructure.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SyncRealEstateRepository:
    def save(self, value: RealEstateModel) -> None:
        try:
            session.add(value)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncRealEstateRepository][save] target_model RealEstateModel error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException

    def update(self, value: RealEstateModel) -> None:
        if isinstance(value, RealEstateModel):
            session.execute(
                update(RealEstateModel)
                .where(RealEstateModel.id == value.id)
                .values(
                    name=value.name,
                    jibun_address=value.jibun_address,
                    road_address=value.road_address,
                    si_do=value.si_do,
                    si_gun_gu=value.si_gun_gu,
                    dong_myun=value.dong_myun,
                    road_name=value.road_name,
                    road_number=value.road_number,
                    land_number=value.land_number,
                    x_vl=value.x_vl,
                    y_vl=value.y_vl,
                    front_legal_code=value.front_legal_code,
                    back_legal_code=value.back_legal_code,
                    is_available=value.is_available,
                )
            )

        session.commit()

    def exists_by_key(self, value: RealEstateModel) -> bool:
        query = select(RealEstateModel.id).where(RealEstateModel.id == value.id)
        result = session.execute(query).scalars().first()

        if result:
            return True

        return False
