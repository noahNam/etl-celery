from sqlalchemy import select, and_
from typing import Type

from modules.adapter.infrastructure.sqlalchemy.database import session
from core.domain.datalake.photo.interface.photo_repository import PhotoRepository

from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_photo_model import (
    PublicSalePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.subscription_info_model import (
    SubscriptionInfoModel
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSalePhotoEntity,
    PublicSaleDtPhotoEntity,
)

logger = logger_.getLogger(__name__)


class SyncPhotoRepository(PhotoRepository):
    def find_all(
            self,
            model: Type[PublicSalePhotoModel | PublicSaleDetailPhotoModel]
    ) -> list[PublicSalePhotoEntity | PublicSaleDtPhotoEntity]:

        if model == PublicSalePhotoModel:
            query = (
                select(
                    model
                ).where(
                    model.update_needed == True
                )
            )
            results = session.execute(query).scalars().all()
            if results:
                result_list = [
                    result.to_entity() for result in results
                ]
                return result_list
            else:
                return list()

        elif model == PublicSaleDetailPhotoModel:
            query = (
                session.query(model).with_entities(
                    model.id,
                    model.file_name,
                    model.path,
                    model.extension,
                    SubscriptionInfoModel.id.label('public_sale_detail_id'),
                ).where(
                    model.update_needed == True
                ).join(
                    SubscriptionInfoModel,
                    and_(
                        model.subs_id == SubscriptionInfoModel.subs_id,
                        model.area_type == SubscriptionInfoModel.area_type
                    ),
                    isouter=True,
                )
            )
            results = query.all()
            if results:
                result_list = [
                    self._to_entity_for_public_sale_dt(result) for result in results
                ]
                return result_list
            else:
                return list()
        else:
            return list()

    def _to_entity_for_public_sale_dt(self, queryset) -> PublicSaleDtPhotoEntity | None:
        if queryset.public_sale_detail_id:
            try:
                return PublicSaleDtPhotoEntity(
                    id=queryset.id,
                    subs_id=queryset.public_sale_detail_id,
                    file_name=queryset.file_name,
                    path=queryset.path,
                    extension=queryset.extension,
                    is_available=True,
                    update_needed=True,
                )
            except:
                print(queryset)
        else:
            return None
