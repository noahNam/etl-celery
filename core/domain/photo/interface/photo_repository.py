from abc import ABC, abstractmethod

from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.house_photo_model import (
    HousePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.house_type_photo_model import (
    HouseTypePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datalake.public_sale_photo_model import (
    PublicSalePhotoModel,
)


class PhotoRepository(ABC):
    @abstractmethod
    def save(
        self,
        model: HousePhotoModel
        | HouseTypePhotoModel
        | PublicSalePhotoModel
        | PublicSaleDetailPhotoModel,
    ) -> None:
        pass
