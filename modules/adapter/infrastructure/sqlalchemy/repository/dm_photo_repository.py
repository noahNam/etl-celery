from sqlalchemy import update, select, and_

from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.adapter.infrastructure.sqlalchemy.database import session
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_photo_model import (
    PublicSalePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_photo_model import (
    PublicSalePhotoModel as MartPublicSalePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel as MartPublicSaleDetailPhotoModel,
)

logger = logger_.getLogger(__name__)


class SyncDMPhotoRepository:
    def save_public_sale_photos(
        self,
        public_sale_photos: list[MartPublicSalePhotoModel],
        public_sale_detail_photos: list[MartPublicSaleDetailPhotoModel],
    ) -> None:
        try:
            for public_sale_photo in public_sale_photos:
                exists_result: bool = self.exists_by_key(value=public_sale_photo)
                if exists_result:
                    self.update(public_sale_photo)
                else:
                    self.save(public_sale_photo)

            for public_sale_detail_photo in public_sale_detail_photos:
                exists_result: bool = self.exists_by_key(value=public_sale_detail_photo)
                if exists_result:
                    self.update(public_sale_detail_photo)
                else:
                    self.save(public_sale_detail_photo)

            session.execute(
                update(PublicSalePhotoModel)
                .where(PublicSalePhotoModel.update_needed == True)
                .values(update_needed=False)
            )

            session.execute(
                update(PublicSaleDetailPhotoModel)
                .where(PublicSaleDetailPhotoModel.update_needed == True)
                .values(update_needed=False)
            )
            session.commit()
        except Exception as e:
            logger.error(
                f"[SyncPublicSaleRepository][save_all_update_needed][error : {e}]"
            )
            session.rollback()
            raise Exception

    def save(
        self,
        model: MartPublicSalePhotoModel | MartPublicSaleDetailPhotoModel,
    ) -> None:
        session.add(model)

    def update(
        self, model: MartPublicSalePhotoModel | MartPublicSaleDetailPhotoModel
    ) -> None:
        if isinstance(model, MartPublicSalePhotoModel):
            session.execute(
                update(MartPublicSalePhotoModel)
                .where(
                    and_(
                        MartPublicSalePhotoModel.public_sale_id == model.public_sale_id,
                        MartPublicSalePhotoModel.file_name == model.file_name,
                    )
                )
                .values(
                    path=model.path,
                    extension=model.extension,
                    is_thumbnail=model.is_thumbnail,
                    seq=model.seq,
                    is_available=model.is_available,
                    update_needed=model.update_needed,
                )
            )
        elif isinstance(model, MartPublicSaleDetailPhotoModel):
            session.execute(
                update(MartPublicSaleDetailPhotoModel)
                .where(
                    and_(
                        MartPublicSaleDetailPhotoModel.public_sale_detail_id
                        == model.public_sale_detail_id,
                        MartPublicSaleDetailPhotoModel.file_name == model.file_name,
                    )
                )
                .values(
                    file_name=model.file_name,
                    path=model.path,
                    extension=model.extension,
                    is_available=model.is_available,
                    update_needed=model.update_needed,
                )
            )

    def exists_by_key(
        self, value: MartPublicSalePhotoModel | MartPublicSaleDetailPhotoModel
    ) -> bool:
        if isinstance(value, MartPublicSalePhotoModel):
            query = select(MartPublicSalePhotoModel.id).where(
                and_(
                    MartPublicSalePhotoModel.public_sale_id == value.public_sale_id,
                    MartPublicSalePhotoModel.file_name == value.file_name,
                )
            )
            result = session.execute(query).scalars().first()
        elif isinstance(value, MartPublicSaleDetailPhotoModel):
            query = select(MartPublicSaleDetailPhotoModel.id).where(
                and_(
                    MartPublicSaleDetailPhotoModel.public_sale_detail_id
                    == value.public_sale_detail_id,
                    MartPublicSaleDetailPhotoModel.file_name == value.file_name,
                )
            )
            result = session.execute(query).scalars().first()
        else:
            result = None

        if result:
            return True
        else:
            return False
