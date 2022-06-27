
from sqlalchemy import exc
from modules.adapter.infrastructure.utils.log_helper import logger_
from exceptions.base import NotUniqueErrorException
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_model import (
    PublicSaleModel
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_model import (
    PublicSaleDetailModel
)

logger = logger_.getLogger(__name__)


class SyncPublicSaleRepository:
    def save_all(self,
                 models: list[PublicSaleModel] | list[PublicSaleDetailModel]
                 ) -> None:
        if not models:
            return None

        try:
            session.add_all(models)
            session.commit()
        except exc.IntegrityError as e:
            logger.error(
                f"[PublicSaleRepository][save_all][{type(models[0])}] updated_at : {models[0].updated_at} error : {e}"
            )
            session.rollback()
            raise NotUniqueErrorException
