import json

from modules.adapter.infrastructure.utils.log_helper import logger_
from modules.application.use_case.etl import BaseETLUseCase
from modules.adapter.infrastructure.sqlalchemy.repository.photo_repository import (
    SyncPhotoRepository,
)
from modules.adapter.infrastructure.sqlalchemy.repository.dm_photo_repository import (
    SyncDMPhotoRepository,
)
from modules.adapter.infrastructure.message.broker.redis import RedisClient
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
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSalePhotoEntity,
    PublicSaleDtPhotoEntity,
)
from modules.adapter.infrastructure.etl.mart_photos import (
    TransformPhotos,
)

logger = logger_.getLogger(__name__)


class PublicSalePhotoUseCase(BaseETLUseCase):
    def __init__(
        self,
        photo_repo: SyncPhotoRepository,
        dm_photo_repo: SyncDMPhotoRepository,
        redis: RedisClient,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._photo_repo: SyncPhotoRepository = photo_repo
        self._dm_photo_repo: SyncDMPhotoRepository = dm_photo_repo
        self._redis: RedisClient = redis
        self._transfer = TransformPhotos()

    def execute(self):
        public_sale_photos: list[PublicSalePhotoEntity] = self._photo_repo.find_all(
            model=PublicSalePhotoModel
        )

        public_sale_detail_photos: list[
            PublicSaleDtPhotoEntity
        ] = self._photo_repo.find_all(model=PublicSaleDetailPhotoModel)

        public_sale_photo_models: list[
            MartPublicSalePhotoModel
        ] = self._transfer.start_etl(target_list=public_sale_photos)

        public_sale_detail_photo_models: list[
            MartPublicSaleDetailPhotoModel
        ] = self._transfer.start_etl(target_list=public_sale_detail_photos)

        self._dm_photo_repo.save_public_sale_photos(
            public_sale_photo_models, public_sale_detail_photo_models
        )

        for public_sale_photo in public_sale_photo_models:
            self.redis_set(model=public_sale_photo)
        for public_sale_detail_photo in public_sale_detail_photo_models:
            self.redis_set(model=public_sale_detail_photo)

    def redis_set(
        self, model: MartPublicSalePhotoModel | MartPublicSaleDetailPhotoModel
    ) -> None:
        # message publish to redis
        if isinstance(model, MartPublicSalePhotoModel):
            ref_table = "public_sale_photos"
            self._redis.set(
                key=f"sync:{ref_table}:{model.public_sale_id}:{model.file_name}",
                value=json.dumps(model.to_dict(), ensure_ascii=False).encode("utf-8"),
            )
        elif isinstance(model, MartPublicSaleDetailPhotoModel):
            ref_table = "public_sale_detail_photos"
            self._redis.set(
                key=f"sync:{ref_table}:{model.public_sale_detail_id}:{model.file_name}",
                value=json.dumps(model.to_dict(), ensure_ascii=False).encode("utf-8"),
            )
        else:
            return None
