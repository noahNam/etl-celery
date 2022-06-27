
from sqlalchemy import exc
from modules.adapter.infrastructure.utils.log_helper import logger_
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)

logger = logger_.getLogger(__name__)


class PublicSaleRepository:
    def save_all(self, insert_models: list[PublicSaleModel]) -> None:
        if not insert_models:
            return None

        try:
            session.add_all(insert_models)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[SyncBuildingDealRepository][save][{type(insert_models[0])}] updated_at : {insert_models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException
