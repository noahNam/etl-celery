from typing import Any

from modules.adapter.infrastructure.sqlalchemy.entity.warehouse.v1.basic_info_entity import (
    BasicInfoEntity,
)
from modules.adapter.infrastructure.sqlalchemy.persistence.model.datamart.real_estate_model import (
    RealEstateModel,
)


class TransformRealEstate:
    def start_etl(
        self,
        from_model: str,
        target_list: list[BasicInfoEntity],
    ) -> list[Any] | None:
        if not target_list:
            return None

        if from_model == "basic_infos":
            return self._etl_basic_infos(target_list)

    def _etl_basic_infos(
        self, target_list: list[BasicInfoEntity]
    ) -> list[RealEstateModel]:
        result = list()
        for target_entity in target_list:
            if not target_entity.place_id:
                continue

            result.append(
                RealEstateModel(
                    id=target_entity.place_id,
                    name=target_entity.bld_name,
                    jibun_address=target_entity.place_dong_address,
                    road_address=target_entity.place_road_address,
                    si_do=target_entity.sido,
                    si_gun_gu=target_entity.sigungu,
                    dong_myun=target_entity.dongri + " " + target_entity.eubmyun,
                    road_name=target_entity.road_name,
                    road_number=target_entity.road_number,
                    land_number=target_entity.land_number,
                    x_vl=target_entity.x_vl,
                    y_vl=target_entity.y_vl,
                    front_legal_code=target_entity.sigungu_cd,
                    back_legal_code=target_entity.bjdong_cd,
                    is_available=target_entity.is_available,
                    update_needed=True
                )
            )
        return result
