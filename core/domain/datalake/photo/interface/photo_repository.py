from abc import ABC, abstractmethod
from typing import Type

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_photo_model import (
    PublicSalePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSalePhotoEntity,
    PublicSaleDtPhotoEntity,
)


class PhotoRepository(ABC):
    @abstractmethod
    def find_all(
        self, model: Type[PublicSalePhotoModel | PublicSaleDetailPhotoModel]
    ) -> list[PublicSalePhotoEntity | PublicSaleDtPhotoEntity]:
        pass
