from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_photo_model import (
    PublicSalePhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.public_sale_detail_photo_model import (
    PublicSaleDetailPhotoModel,
)
from modules.adapter.infrastructure.sqlalchemy.entity.datalake.v1.photo_entity import (
    PublicSalePhotoEntity,
    PublicSaleDtPhotoEntity,
)


class TransformPhotos:
    def start_etl(
        self,
        target_list: list[PublicSalePhotoEntity | PublicSaleDtPhotoEntity],
    ) -> list[PublicSalePhotoModel | PublicSaleDetailPhotoModel]:

        if not target_list:
            return list()

        if isinstance(target_list[0], PublicSalePhotoEntity):
            results = list()
            for target in target_list:
                result = PublicSalePhotoModel(
                    public_sale_id=target.subs_id,
                    file_name=target.file_name,
                    path=target.path,
                    extension=target.extension,
                    is_thumbnail=target.is_thumbnail,
                    seq=target.seq,
                    is_available=True,
                    update_needed=True,
                )
                results.append(result)

        elif isinstance(target_list[0], PublicSaleDtPhotoEntity):
            results = list()
            for target in target_list:
                result = PublicSaleDetailPhotoModel(
                    public_sale_detail_id=target.subs_id,
                    file_name=target.file_name,
                    path=target.path,
                    extension=target.extension,
                    is_available=True,
                    update_needed=True,
                )
                results.append(result)
        else:
            return list()
        return results
